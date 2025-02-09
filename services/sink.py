from abc import ABC, abstractmethod


class Sink(ABC):
    @abstractmethod
    def get(self, query):
        pass

    @abstractmethod
    def put(self, record):
        pass


class DatabaseSink:
    def __init__(self, creds=None, instance=None):
        self.creds = creds
        self.instance = instance

    def get(self, query):
        print("Got the request")
        return None

    def put(self, record):
        print("Got the record")
        return False


class SinkService:
    def __init__(self):
        self.db_sink = None
        self.file_sink = None
        self.cache_sink = None

    def create_sink(self, sink_type):

        if sink_type == "db_sink":
            self.db_sink = DatabaseSink()
        else:
            pass
