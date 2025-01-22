class MyMetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=MyMetaSingleton):
    pass

if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    print(s1 is s2)
    print(s1 == s2)
    print(id(s1) == id(s2))