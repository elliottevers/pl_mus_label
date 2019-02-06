import pytest
from message import messenger


class TestMessenger:
    def test_messaging(self):
        mes = messenger.Messenger('key')
        assert mes._key_route == 'key'
