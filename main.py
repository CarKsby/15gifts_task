from fifteen_gifts_task.extractor import JSONFileExtractor
from fifteen_gifts_task.transformer.handset_transformer import HandsetTransformer
from fifteen_gifts_task.transformer.extras_transformer import ExtrasTransformer
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
    session = loader.get_session()
    raw_data = JSONFileExtractor().extract(
        "src/fifteen_gifts_task/resources/singleton.json"
    )
    handset_transformer = HandsetTransformer(raw_data)
    extras_transformer = ExtrasTransformer(raw_data)
    handset_tariff_transformer = HandsetTariffTransformer(raw_data)
    handset_colour_transformer = HandsetColourTransformer(raw_data)

    handset_transformer.transform()
    extras_transformer.transform()
    handset_tariff_transformer.transform()
    handset_colour_transformer.transform()

    # print(handset_colour_transformer.transformed_models_list)
    # print(extras_transformer.transformed_models_list)
    # for tariff in handset_tariff_transformer.transformed_models_list:   
    #     print(tariff.model_dump()["planOfferingCode"])
    #     for extra in tariff.tariffExtras:
    #         print(f"  - {extra.model_dump()}")
    # print(handset_transformer.transformed_models_list)

    extras_transformer.set_table_models()
    extra_rows = extras_transformer.get_table_models()
    loader.load_extras(extra_rows, session)


    handset_tariff_transformer.set_table_models(session)
    tariff_table_models = handset_tariff_transformer.get_table_models()

    

    loader.load_tariffs(tariff_table_models, session)

    # handset_colour_transformer.set_table_models()
    # colour_table_models = handset_colour_transformer.get_table_models()

    # handset_transformer.set_table_models()
    # handset_table_model = handset_transformer.get_table_models()[0]

    # handset_table_model.handsetColours = colour_table_models
    # handset_table_model.handsetTariffs = tariff_table_models
    # loader.load_handsets(handset_table_model)

    
    



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
