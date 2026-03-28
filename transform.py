import pandas as pd

def transform_data(df):
    try:
        # -------------------------------
        # 1. Clean column names (VERY IMPORTANT)
        # -------------------------------
        df.columns = (
            df.columns
            .str.strip()            # remove spaces
            .str.replace(" ", "")   # remove internal spaces
            .str.lower()            # make lowercase
        )

        print("Columns after cleaning:", df.columns.tolist())

        # -------------------------------
        # 2. Drop duplicates
        # -------------------------------
        df = df.drop_duplicates()

        # -------------------------------
        # 3. Remove missing customerid
        # -------------------------------
        df = df.dropna(subset=['customerid'])

        # -------------------------------
        # 4. Remove invalid values
        # -------------------------------
        df = df[df['quantity'] > 0]
        df = df[df['unitprice'] > 0]

        # -------------------------------
        # 5. Convert date
        # -------------------------------
        df['invoicedate'] = pd.to_datetime(df['invoicedate'], errors='coerce')
        df = df.dropna(subset=['invoicedate'])

        # -------------------------------
        # 6. Create SalesAmount
        # -------------------------------
        df['salesamount'] = df['quantity'] * df['unitprice']

        # -------------------------------
        # 7. Fact table
        # -------------------------------
        fact_sales = df[[
            'invoiceno',
            'stockcode',
            'customerid',
            'quantity',
            'unitprice',
            'invoicedate',
            'salesamount'
        ]].copy()

        # -------------------------------
        # 8. Dimension tables
        # -------------------------------
        dim_products = df[['stockcode', 'description']].drop_duplicates().copy()
        dim_customers = df[['customerid', 'country']].drop_duplicates().copy()

        print("✅ Data transformed successfully")

        return fact_sales, dim_products, dim_customers

    except Exception as e:
        print(f"❌ Error in transformation: {e}")
        return None, None, None


# -------------------------------
# TEST BLOCK
# -------------------------------
if __name__ == "__main__":
    from extract import extract_data

    df = extract_data()

    if df is not None:
        fact, products, customers = transform_data(df)

        if fact is not None:
            print("\n📊 Fact Table:")
            print(fact.head())

            print("\n📦 Products:")
            print(products.head())

            print("\n👤 Customers:")
            print(customers.head())