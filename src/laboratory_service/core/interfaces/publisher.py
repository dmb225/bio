from abc import ABC, abstractmethod


class PublisherPort(ABC):
    @abstractmethod
    def publish(self, message: dict):
        pass

