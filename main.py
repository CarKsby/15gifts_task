from fifteen_gifts_task.extractor import JSONFileExtractor
from fifteen_gifts_task.transformer.handset_transformer import HandsetTransformer
from fifteen_gifts_task.transformer.handset_colour_transformer import (
    HandsetColourTransformer,
)
from fifteen_gifts_task.transformer.handset_tariff_transformer import (
    HandsetTariffTransformer,
)
from fifteen_gifts_task.loader import Loader
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    loader = Loader()
    product_set = JSONFileExtractor().extract(
        "src/fifteen_gifts_task/resources/o2-product-set.json"
    )
    for product in product_set:
        logging.info(f"Transforming product {product["name"]}")
        handset_transformer = HandsetTransformer(product)
        handset_tariff_transformer = HandsetTariffTransformer(product)
        handset_colour_transformer = HandsetColourTransformer(product)

        handset_transformer.transform()
        handset_tariff_transformer.transform()
        handset_colour_transformer.transform()


        handset_tariff_transformer.set_table_models()
        tariff_table_models = handset_tariff_transformer.get_table_models()

        handset_colour_transformer.set_table_models()
        colour_table_models = handset_colour_transformer.get_table_models()

        handset_transformer.set_table_models()
        handset_table_model = handset_transformer.get_table_models()[0]

        handset_table_model.handsetColours = colour_table_models
        handset_table_model.handsetTariffs = tariff_table_models
        loader.load_handsets(handset_table_model)

    
    



    db_path = "o2_inventory.sqlite3"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    logging.info(f"\n📋 Tables found in {db_path}: {tables}")

    for table in tables:
        print(f"\n🔎 Top 100 rows from '{table}':")
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 100;")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            # Print column headers and first few rows
            print(" | ".join(columns))
            for row in rows:
                print(row)

            if not rows:
                print("(No rows found)")
        except sqlite3.Error as e:
            print(f"⚠️ Error reading from {table}: {e}")

    # Clean up
    conn.close()
