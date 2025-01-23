from functools import wraps


class PermissionError(Exception):
    @property
    def message(self):
        return 'Permission Error'


class MyRequest:
    def __init__(self, role: str):
        self.role = role


def access_control(roles: list[str]):
    def wrapper1(func):
        @wraps(func)
        def wrapper2(request: MyRequest):
            if request.role in roles:
                return func(request)
            else:
                raise PermissionError
        return wrapper2
    return wrapper1


@access_control(roles=['admin', 'moderator'])
def my_func(request: MyRequest):
    print(f'{request.role} is working...')


if __name__ == '__main__':
    r1 = MyRequest('admin')
    r2 = MyRequest('moderator')
    r3 = MyRequest('anonim')

    try:
        my_func(r1)
        my_func(r2)
        my_func(r3)
    except PermissionError as err:
        print(err.message)
