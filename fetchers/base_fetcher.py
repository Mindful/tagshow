import abc


class BaseFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch(self):
        pass