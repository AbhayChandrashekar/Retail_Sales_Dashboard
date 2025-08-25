import pandas as pd
from sqlalchemy import create_engine, text
import os


MYSQL_USER = 'jack'
MYSQL_PASSWORD = 'jack'
MYSQL_HOST = 'localhost' 
MYSQL_DB = 'retail_sales_db'
# -------------------------------

def run_retail_etl(raw_data_path='data/raw_sales_data.csv',
                   catalog_path='data/product_catalog.xlsx',
                   cleaned_csv_output='data/cleaned_sales_data.csv'):

    print("Starting ETL process...")

    os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)

    try:
        sales_df = pd.read_csv(raw_data_path)
        catalog_df = pd.read_excel(catalog_path)
        print("Raw data and catalog loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading files: {e}. Make sure generate_data.py was run.")
        return

    print("Performing data cleaning and transformations...")

    sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'])
    sales_df['Year'] = sales_df['OrderDate'].dt.year
    sales_df['Month'] = sales_df['OrderDate'].dt.month
    sales_df['Day'] = sales_df['OrderDate'].dt.day
    sales_df['DayOfWeek'] = sales_df['OrderDate'].dt.day_name()
    sales_df['HourOfDay'] = sales_df['OrderDate'].dt.hour
    sales_df['Quarter'] = sales_df['OrderDate'].dt.quarter
    sales_df['MonthYear'] = sales_df['OrderDate'].dt.to_period('M').astype(str)

    sales_df.dropna(subset=['ProductName', 'ProductCategory', 'TotalPrice', 'Quantity'], inplace=True)

    for col in ['PricePerUnit', 'Quantity', 'TotalPrice', 'TargetSales']:
        sales_df[col] = pd.to_numeric(sales_df[col], errors='coerce').fillna(0)

    sales_df['Profit'] = sales_df['TotalPrice'] * 0.25
    sales_df = pd.merge(sales_df, catalog_df[['ProductName', 'Brand']], on='ProductName', how='left')

    sales_df = sales_df[sales_df['TotalPrice'] > 0]
    sales_df = sales_df[sales_df['Quantity'] > 0]

    print(f"Cleaned data shape: {sales_df.shape}")

    print(f"Connecting to MySQL database: {MYSQL_DB} on {MYSQL_HOST}...")
    try:
        engine = create_engine(f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Successfully connected to MySQL.")

        sales_table_ddl = """
        CREATE TABLE IF NOT EXISTS sales_data (
            OrderID VARCHAR(50) PRIMARY KEY,
            CustomerID VARCHAR(50),
            OrderDate DATETIME,
            ProductName VARCHAR(255),
            ProductCategory VARCHAR(100),
            PricePerUnit DECIMAL(10,2),
            Quantity INT,
            TotalPrice DECIMAL(10,2),
            City VARCHAR(100),
            PaymentMethod VARCHAR(100),
            SalesChannel VARCHAR(100),
            TargetSales DECIMAL(10,2),
            Year INT,
            Month INT,
            Day INT,
            DayOfWeek VARCHAR(20),
            HourOfDay INT,
            Quarter INT,
            MonthYear VARCHAR(10),
            Profit DECIMAL(10,2),
            Brand VARCHAR(255)
        );
        """

        product_catalog_ddl = """
        CREATE TABLE IF NOT EXISTS product_catalog (
            ProductName VARCHAR(255) PRIMARY KEY,
            ProductCategory VARCHAR(100),
            PricePerUnit DECIMAL(10,2),
            ProductSKU VARCHAR(50),
            Brand VARCHAR(255)
        );
        """

        with engine.connect() as connection:
            print("Creating/updating sales_data table schema...")
            connection.execute(text(sales_table_ddl))
            print("Creating/updating product_catalog table schema...")
            connection.execute(text(product_catalog_ddl))
            connection.commit() # Commit DDL changes

        print("Loading sales data into MySQL...")
        sales_df.to_sql('sales_data', con=engine, if_exists='replace', index=False, chunksize=1000)
        print("Loading product catalog into MySQL...")
        catalog_df.to_sql('product_catalog', con=engine, if_exists='replace', index=False, chunksize=1000)

        print(f"Cleaned data saved to MySQL database: {MYSQL_DB}")

    except Exception as e:
        print(f"Error connecting to or loading data into MySQL: {e}")
        print("Please ensure MySQL is running, credentials are correct, and the database/user exist.")
        print("If you get a 'No module named 'MySQLdb'' error, try 'pip install pymysql' and change 'mysql+mysqlclient' to 'mysql+pymysql' in create_engine.")
    
        print("Falling back to saving as CSV for Power BI connection...")
        sales_df.to_csv(cleaned_csv_output, index=False)
        print(f"Cleaned data also saved to CSV: {cleaned_csv_output}")
        return

    sales_df.to_csv(cleaned_csv_output, index=False)
    print(f"Cleaned data also saved to CSV: {cleaned_csv_output}")
    print("ETL process completed successfully.")

if __name__ == "__main__":
    print("Checking for raw data generation...")
    if not os.path.exists('data/raw_sales_data.csv') or not os.path.exists('data/product_catalog.xlsx'):
        print("Raw data not found. Running generate_data.py first.")
        import generate_data
        sales_df_generated = generate_data.generate_retail_data(30000)
        sales_df_generated.to_csv('data/raw_sales_data.csv', index=False)

        unique_products = sales_df_generated[['ProductName', 'ProductCategory', 'PricePerUnit']].drop_duplicates().reset_index(drop=True)
        unique_products['ProductSKU'] = [f"SKU{i+1000}" for i in range(len(unique_products))]
        unique_products['Brand'] = [generate_data.fake.company() for _ in range(len(unique_products))]
        unique_products.to_excel('data/product_catalog.xlsx', index=False)
        print("Raw data regenerated.")

    run_retail_etl()