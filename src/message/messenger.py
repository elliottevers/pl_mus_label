from typing import List


class Messenger:

    env: str

    _key_route: str

    def __init__(self, key_route: str = ''):
        self._key_route = key_route

    def message(self, message: List[str]):
        print(' '.join([self._key_route] + message))
