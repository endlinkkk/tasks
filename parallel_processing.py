import concurrent.futures
import logging
import multiprocessing
import random
from datetime import datetime
from functools import wraps

COUNT = 100000
logging.basicConfig(
    filename='result.csv',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def generate_data(n: int) -> list[int]:
    return [random.randint(1, 1000) for _ in range(n)]

def process_number(number: int) -> int:
    factorial = 1
    while number > 1:
        factorial *= number
        number -= 1
    return factorial


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now() - start
        logger.info(f"{func.__name__}; Lead time (ms): {end.microseconds / 1000}")
    return wrapper



# А - Пул потоков
@timer
def test_A():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_number, generate_data(COUNT))


# B - Пул процессов
@timer
def test_B():
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(process_number, generate_data(COUNT))


def producer(q: multiprocessing.Queue):
    for number in generate_data(COUNT):
        q.put(number)
    q.put(None)

def consumer(q: multiprocessing.Queue):
    while True:
        item = q.get()
        if item is None:
            break
        process_number(item)



# C - Отдельные процессы и очереди
@timer
def test_C():

    q = multiprocessing.Queue()
    process1 = multiprocessing.Process(target=producer, args=(q,))
    process2 = multiprocessing.Process(target=consumer, args=(q,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()


# D - Один поток
@timer
def test_D():
    data = generate_data(COUNT)
    for number in data:
        process_number(number)



if __name__ == '__main__':
    test_A()
    test_B()
    test_C()
    test_D()
