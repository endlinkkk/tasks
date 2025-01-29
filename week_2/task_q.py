import multiprocessing
import os

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
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                task_name TEXT NOT NULL,
                status TEXT,
                worker_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        con.commit()
    finally:
        if con:
            con.close()

def fill_table() -> None:
    tasks = [
        ("Обработать заказ", "pending", None),
        ("Проверить доставку", "processing", None),
        ("Сформировать отчет", "completed", None),
        ("Обновить каталог", "pending", None),
        ("Проверить оплату", "processing", None),
        ("Обработать заказ", "pending", None),
        ("Обработать заказ", "pending", None),
        ("Обработать заказ", "pending", None),
    ]
    try:
        con = psycopg2.connect(**connection_params)
        cur = con.cursor()
        for task in tasks:
            cur.execute(
                """
                INSERT INTO tasks (task_name, status, worker_id)
                VALUES (%s, %s, %s)
            """,
                task,
            )
        con.commit()

    finally:
        if con:
            con.close()

def complete_task(task_id) -> None:
    try:
        con = psycopg2.connect(**connection_params)
        cur = con.cursor()
        cur.execute("""
            SELECT * FROM tasks WHERE id = %s FOR UPDATE;
        """, (task_id,))

        cur.execute("""
            UPDATE tasks SET status = 'completed', updated_at = CURRENT_TIMESTAMP
            WHERE id = %s;
        """, (task_id,))
        con.commit()

    finally:
        if con:
            con.close()

def fetch_task() -> None:
    worker_id = os.getpid()
    try:
        con = psycopg2.connect(**connection_params)
        cur = con.cursor()
        cur.execute("""
            SELECT id FROM tasks WHERE status = 'pending' LIMIT 1 FOR UPDATE SKIP LOCKED;
        """)
        task = cur.fetchone()
        if task:
            task_id = task[0]
            cur.execute("""
                UPDATE tasks SET status = 'processing', updated_at = CURRENT_TIMESTAMP, worker_id = %s
                WHERE id = %s AND worker_id IS NULL;
            """, (worker_id, task_id,))
        con.commit()
        if task and task_id:
            complete_task(task_id)

    finally:
        if con:
            con.close()


def start_process(c_processes: int) -> None:
    processes: list[multiprocessing.Process] = []
    for _ in range(c_processes):
        p = multiprocessing.Process(target=fetch_task)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    create_table()
    fill_table()
    start_process(8)
