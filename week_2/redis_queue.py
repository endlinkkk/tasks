import pickle

from redis import Redis


class RedisClient:
    host: str = 'localhost'
    port: int = 6389

    @property
    def get_redis(self) -> Redis:
        return Redis(host=self.host, port=self.port)


class RedisQueue:
    def __init__(self, client: RedisClient):
        self.client = client.get_redis

    def publish(self, msg: dict):
        self.client.rpush('q', pickle.dumps(msg))

    def consume(self) -> dict:
        data = self.client.lpop('q')
        if data:
            return pickle.loads(data)


if __name__ == '__main__':
    rc = RedisClient()
    q = RedisQueue(client=rc)
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
    print('Good')
