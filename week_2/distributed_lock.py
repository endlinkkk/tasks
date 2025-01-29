import datetime
import multiprocessing
import os
import time
from functools import wraps

from redis import Redis
from redis.exceptions import LockError

redis_client = Redis(host="localhost", port=6389, db=0)


def single(max_processing_time: datetime):
    def wrapper1(function):
        @wraps(function)
        def wrapper2(*args, **kwargs):
            lock_name = f"lock:{function.__name__}"
            lock = redis_client.lock(lock_name, timeout=max_processing_time.seconds)
            try:
                acquired = lock.acquire(blocking=False)
                if not acquired:
                    return "Function is locked by another process"

                result = function(*args, **kwargs)
                return result
            finally:
                try:
                    lock.release()
                except LockError:
                    pass

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
    start_process(2)
