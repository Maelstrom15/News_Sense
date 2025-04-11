import json
import sqlite3
import os

DATA_PATH = "data"
DB_PATH = "database/news_sense.db"

def load_json_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    files = ["mutual_funds.json", "stocks.json", "holdings.json"]
    for file in files:
        path = os.path.join(DATA_PATH, file)
        with open(path, "r") as f:
            data = json.load(f)
            table = os.path.splitext(file)[0]
            if isinstance(data, list) and data:
                columns = data[0].keys()
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                cursor.execute(f"CREATE TABLE {table} ({', '.join([col + ' TEXT' for col in columns])})")
                for row in data:
                    cursor.execute(
                        f"INSERT INTO {table} VALUES ({','.join(['?' for _ in columns])})",
                        tuple(row.values())
                    )
    conn.commit()
    conn.close()