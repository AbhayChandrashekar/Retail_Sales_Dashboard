import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_IN')

def generate_retail_data(num_rows=30000):
    products = {
        'Laptop': 1200, 'Smartphone': 800, 'Headphones': 150, 'Keyboard': 75,
        'Mouse': 30, 'Monitor': 300, 'Webcam': 50, 'Router': 90,
        'Printer': 200, 'Speaker': 100, 'External SSD': 120, 'Smartwatch': 250,
        'Tablet': 350, 'Gaming Console': 400, 'VR Headset': 600, 'Smart Home Hub': 120
    }
    product_categories = {
        'Laptop': 'Electronics', 'Smartphone': 'Electronics', 'Headphones': 'Audio & Accessories',
        'Keyboard': 'Audio & Accessories', 'Mouse': 'Audio & Accessories', 'Monitor': 'Electronics',
        'Webcam': 'Audio & Accessories', 'Router': 'Networking', 'Printer': 'Peripherals',
        'Speaker': 'Audio & Accessories', 'External SSD': 'Storage', 'Smartwatch': 'Wearables',
        'Tablet': 'Electronics', 'Gaming Console': 'Gaming', 'VR Headset': 'Gaming', 'Smart Home Hub': 'Smart Home'
    }
    cities = ['Bengaluru', 'Mumbai', 'Delhi', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash On Delivery']
    channels = ['Online Store', 'Physical Store', 'Mobile App', 'Direct Sales']

    data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 1, 1)

    for i in range(num_rows):
        order_id = f"ORD{100000 + i}"
        customer_id = f"CUST{np.random.randint(1000, 5000)}"
        order_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        product_name = random.choice(list(products.keys()))
        price_per_unit = products[product_name]
        quantity = np.random.randint(1, 5)
        total_price = round(price_per_unit * quantity, 2)
        product_category = product_categories[product_name]
        city = random.choice(cities)
        payment_method = random.choice(payment_methods)
        sales_channel = random.choice(channels)

        target_sales = round(total_price * (1 + np.random.uniform(-0.08, 0.12)), 2)

        data.append([
            order_id, customer_id, order_date, product_name, product_category,
            price_per_unit, quantity, total_price, city, payment_method,
            sales_channel, target_sales
        ])

    df = pd.DataFrame(data, columns=[
        'OrderID', 'CustomerID', 'OrderDate', 'ProductName', 'ProductCategory',
        'PricePerUnit', 'Quantity', 'TotalPrice', 'City', 'PaymentMethod',
        'SalesChannel', 'TargetSales'
    ])
    return df

if __name__ == "__main__":
    print("Generating raw sales data...")
    sales_df = generate_retail_data(30000)
    sales_df.to_csv('data/raw_sales_data.csv', index=False)
    print("Generated raw_sales_data.csv in 'data' folder.")

    unique_products = sales_df[['ProductName', 'ProductCategory', 'PricePerUnit']].drop_duplicates().reset_index(drop=True)
    unique_products['ProductSKU'] = [f"SKU{i+1000}" for i in range(len(unique_products))]
    unique_products['Brand'] = [fake.company() for _ in range(len(unique_products))]

    unique_products.to_excel('data/product_catalog.xlsx', index=False)
    print("Generated product_catalog.xlsx in 'data' folder.")