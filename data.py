import os
import pandas as pd

# -------------------------------
# STEP 1: Create Data Folder
# -------------------------------
os.makedirs("Data", exist_ok=True)

# -------------------------------
# STEP 2: Download Dataset (Kaggle API required)
# -------------------------------
print("Downloading dataset...")

os.system(
    "kaggle datasets download -d mohammadtalib786/retail-sales-dataset -p Data --unzip"
)

print("Download complete!")

# -------------------------------
# STEP 3: Load Dataset
# -------------------------------
file_path = "Data/retail_sales_dataset.csv"

df = pd.read_csv(file_path)

print("\nRaw Data Preview:")
print(df.head())

# -------------------------------
# STEP 4: Data Cleaning
# -------------------------------
print("\nCleaning data...")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.dropna(inplace=True)

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert date column (if exists)
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

print("Cleaning complete!")

# -------------------------------
# STEP 5: Create Dimension Tables
# -------------------------------

print("\nCreating dimension tables...")

# Customers Table
if "customer_id" in df.columns:
    customers = df[["customer_id"]].drop_duplicates()
    customers["customer_name"] = "Unknown"  # placeholder

# Products Table
if "product_category" in df.columns:
    products = df[["product_category"]].drop_duplicates()
    products["product_id"] = range(1, len(products) + 1)

    # Map product_id back to main df
    df = df.merge(products, on="product_category", how="left")

# -------------------------------
# STEP 6: Create Fact Table (Orders)
# -------------------------------
print("Creating fact table...")

orders = df.copy()

# Rename columns for clarity
orders.rename(columns={
    "transaction_id": "order_id"
}, inplace=True)

# -------------------------------
# STEP 7: Save Processed Data
# -------------------------------
print("\nSaving processed data...")

customers.to_csv("Data/customers.csv", index=False)
products.to_csv("Data/products.csv", index=False)
orders.to_csv("Data/orders.csv", index=False)

print("\n✅ ETL Process Completed Successfully!")