import time
from colorama import Fore
import psycopg2


con = psycopg2.connect(dbname='n47', user='postgres', host='localhost', password='123')


class Timer:
    def __enter__(self):
        self.s = time.time()
        for i in range(1, 100000):
            print(i*2)
        self.e = time.time()
        return 'Finished'

    def __exit__(self, exc_type, exc_val, exc_tb):

        print((self.e - self.s), 's')


def activate_timer() -> None:
    with Timer() as t:
        print('Executing')
        print(t)


class Queries:
    def __enter__(self):
        print(Fore.GREEN, 'Before updating.', Fore.RESET)
        self.cur1 = con.cursor()
        self.cur1.execute('SELECT * FROM products ORDER BY id;')
        self.rows = self.cur1.fetchall()
        for row in self.rows:
            print(row)
        return self.cur1

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Fore.GREEN, 'After updating.', Fore.RESET)
        self.cur1.execute('SELECT * FROM products ORDER BY id;')
        self.rows2 = self.cur1.fetchall()
        for row in self.rows2:
            print(row)
        print('Finished')


def activate_queries() -> None:
    with Queries() as cur:
        cur.execute('''UPDATE products SET title = 'tennis ball',
                       images = 'https//: tennis ball' WHERE id IN(2,4,6);''')
        cur.execute("""DELETE FROM products WHERE id IN(13,15);""")
        cur.execute("""UPDATE products SET description = 'pink vase made from porcelain' WHERE id in(2,4,6);""")
        con.commit()
        print('done')
