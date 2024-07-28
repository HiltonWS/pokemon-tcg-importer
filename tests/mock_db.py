from unittest import mock


class MockConnection:
    def __init__(self):
        self.execute = mock.Mock()
        self.executescript = mock.Mock()
        self.commit = mock.Mock()
        self.close = mock.Mock()

    def cursor(self):
        return mock.Mock()


def get_mock_connection():
    return MockConnection()
