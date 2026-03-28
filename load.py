from sqlalchemy import create_engine

def load_data(fact_sales, dim_products, dim_customers):
    try:
        # 🔑 Replace password with your MySQL password
        engine = create_engine(
            "mysql+pymysql://root:1234@localhost:3306/retail_db"
        )

        # Load dimension tables first
        dim_products.to_sql('dim_products', engine, if_exists='replace', index=False)
        dim_customers.to_sql('dim_customers', engine, if_exists='replace', index=False)

        # Load fact table
        fact_sales.to_sql('fact_sales', engine, if_exists='replace', index=False)

        print("✅ Data loaded successfully into MySQL")

    except Exception as e:
        print(f"❌ Error in loading: {e}")