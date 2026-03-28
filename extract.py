import pandas as pd

def extract_data(file_path="C:/Users/vijay/OneDrive/Documents/OneDrive/Desktop/Retail ETL Data Pipeline/Data/retail_sales_dataset.csv"):
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            on_bad_lines='skip',
            engine='python'
        )
        print("✅ Data extracted successfully")
        return df

    except Exception as e:
        print(f"❌ Error in extraction: {e}")
        return None


if __name__ == "__main__":
    df = extract_data()

    if df is not None:
        print(df.head())