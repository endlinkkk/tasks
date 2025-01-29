import random
import time
from uuid import uuid4

from redis import Redis


class RedisClient:
    host: str = "localhost"
    port: int = 6389

    @property
    def get_redis(self) -> Redis:
        return Redis(host=self.host, port=self.port)


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, client: RedisClient):
        self.client = client.get_redis

    def test(self) -> bool:
        if self.client.dbsize() >= 5:
            return False
        self.client.setex(name=str(uuid4()), time=3, value=0)
        return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    rc = RedisClient()
    rate_limiter = RateLimiter(rc)

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
