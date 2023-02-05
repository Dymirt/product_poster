import sqlite3
from sqlite3 import Error
from datetime import datetime

database_file = "./database.db"

sql_create_table = """ CREATE TABLE IF NOT EXISTS products (
                                    UtilityId INTEGER PRIMARY KEY,
                                    product_id INTEGER NOT NULL,
                                    date TEXT NOT NULL
                                ); """

sql_add_product = "INSERT INTO products (product_id, date) values(?,?)"


DATABASE = sqlite3.connect(database_file)
cur = DATABASE.cursor()
cur.execute(sql_create_table)


def add(product: int):
    product = (
        product,
        f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year}",
    )
    try:
        cur.execute(sql_add_product, product)
        DATABASE.commit()
    except Error as e:
        print(e)


def get_all_id():
    cur.execute("SELECT product_id FROM products")
    products_id = []
    for i in cur.fetchall():
        products_id.append(i[0])
    return products_id
