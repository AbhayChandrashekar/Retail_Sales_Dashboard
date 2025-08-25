# 🛒 Retail Sales Dashboard

An end-to-end data pipeline that **generates synthetic retail sales data**, **transforms it via ETL**, and **visualizes insights in Power BI**.

This project simulates real-world analytics workflows — from raw data to actionable dashboards.

---

## 📁 Project Structure

| File                          | Purpose                                                             |
| ----------------------------- | ------------------------------------------------------------------- |
| `generate_data.py`            | Generates realistic synthetic sales data using `Faker` and `pandas` |
| `etl_pipeline.py`             | Cleans, enriches, and loads data into MySQL and CSV                 |
| `data/raw_sales_data.csv`     | Raw transactional sales data                                        |
| `data/product_catalog.xlsx`   | Product master data                                                 |
| `data/cleaned_sales_data.csv` | Output of ETL for Power BI                                          |
| `Retail_sales_dashboard.pbix` | Interactive Power BI dashboard                                      |

---

## ⚙️ How It Works

### 1. **Data Generation**

- Generates **30,000+ sales transactions** with realistic:
  - Products (Laptops, Smartphones, etc.)
  - Categories, prices, quantities
  - Order dates (2023–2025)
  - Cities (Indian metro cities)
  - Payment methods (UPI, Credit Card, etc.)
  - Sales channels (Online, Mobile App, etc.)

### 2. **ETL Pipeline**

- Parses and cleans data
- Adds **time-based features**:
  - Year, Month, Day, Hour, Quarter
  - Day of Week, Month-Year
- Calculates **Profit** (25% of TotalPrice)
- Merges with **product catalog** to add `Brand`
- Filters invalid records (zero price/quantity)
- Loads into:
  - **MySQL database** (`retail_sales_db`)
  - **CSV file** (for Power BI)

### 3. **Power BI Dashboard**

- Connects to `cleaned_sales_data.csv`
- Visualizes:
  - Sales trends over time
  - Top products & categories
  - City-wise performance
  - Payment method distribution
  - Profit vs Target Sales
  - Channel-wise comparison

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/AbhayChandrashekar/Retail_Sales_Dashboard.git
cd Retail_Sales_Dashboard

pip install pandas numpy pymysql sqlalchemy faker openpyxl

Ensure MySQL is running and update credentials in etl_pipeline.py

python etl_pipeline.py

Open Retail_sales_dashboard.pbix in Power BI Desktop to view insights.



```
