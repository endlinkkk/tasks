from datetime import datetime


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now() 
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMeta):
    pass


if __name__ == '__main__':
    o = MyClass()
    assert hasattr(o, 'created_at')
