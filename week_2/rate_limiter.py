import random
import time

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
    key = "api_rate_limiter"

    def __init__(self, client: RedisClient):
        self.client = client.get_redis

    def test(self) -> bool:
        try:
            current_time = int(time.time())
            to_remove = []

            for t in self.client.smembers(self.key):
                if (current_time - int(t)) > 3:
                    to_remove.append(t)

            for t in to_remove:
                self.client.srem(self.key, t)

            if self.client.scard(self.key) > 3:
                return False

            cur_unix_time = current_time
            self.client.sadd(self.key, cur_unix_time)
            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False


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
        time.sleep(random.randint(0, 1))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
