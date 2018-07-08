from abc import ABC,abstractmethod


class Pusher(ABC):
    @abstractmethod
    def send_message(self, thread, message):
        pass