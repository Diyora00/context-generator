import os
import psycopg2
from colorama import Fore
from dotenv import load_dotenv, dotenv_values

load_dotenv()
db_params = {
    'database': os.getenv('database'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}

# conn = psycopg2.connect(**db_params)


class Product:
    def __init__(self, title: str, category: str, price: float, stoke: int):
        self.title = title
        self.category = category
        self.price = price
        self.stoke = stoke


class ConnectDB:
    def __init__(self):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT * FROM product;""")
        for row in self.cur.fetchall():
            print(row)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.conn.rollback()
        if self.conn:
            self.cur.close()
            self.conn.close()

    def commit(self) -> None:
        self.conn.commit()


def save_to_product() -> None:
    try:
        with ConnectDB() as db:
            t = input('Input title: ')
            c = input('Input category: ')
            p = float(input('Input price: '))
            s = int(input('Input stoke: '))
            p1 = Product(t, c, p, s)
            data = (p1.title, p1.category, p1.price, p1.stoke)
            s_q = """INSERT INTO product (title, category, price, stoke) VALUES (%s, %s, %s, %s)"""
            db.cur.execute(s_q, data)
            db.commit()
            print(Fore.GREEN, 'Successfully saved.', Fore.RESET)
    except Exception as e:
        print(Fore.RED, e, Fore.RESET)
