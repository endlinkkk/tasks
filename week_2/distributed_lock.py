import datetime
import multiprocessing
import os
import time
from functools import wraps

import psycopg2

connection_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5433'      
}



def create_table() -> None:
    try:
        con = psycopg2.connect(**connection_params)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS funcs (
                id SERIAL PRIMARY KEY,
                func_name TEXT NOT NULL
            )
        """)
        con.commit()
    finally:
        if con:
            con.close()



def insert_func() -> None:
    con = psycopg2.connect(**connection_params)
    cur = con.cursor()
    cur.execute(
                """
                INSERT INTO funcs (func_name) VALUES ('process_transaction');
                """
            )
    con.commit()

def single(max_processing_time: datetime):
    def wrapper1(function):
        @wraps(function)
        def wrapper2(*args, **kwargs):
            con = psycopg2.connect(**connection_params)
            cur = con.cursor()
            cur.execute("""
            SET LOCAL lock_timeout = %s;
            SELECT * FROM funcs WHERE func_name = %s FOR UPDATE SKIP LOCKED;
        """, (str(max_processing_time.seconds), function.__name__,))
            func_metadata = cur.fetchone()
            if func_metadata:
                print(os.getpid())
                res = function(*args, **kwargs)
                return res
        return wrapper2
    return wrapper1


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    print(os.getpid())
    time.sleep(2)



def start_process(c_processes: int) -> None:
    processes: list[multiprocessing.Process] = []
    for _ in range(c_processes):
        p = multiprocessing.Process(target=process_transaction)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    create_table()
    insert_func()
    start_process(8)
