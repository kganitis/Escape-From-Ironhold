# properties.py
from abc import ABC, abstractmethod


# result types
SUCCESS = "SUCCESS"  # result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
ERROR = "ERROR"  # invalid command


class Usable(ABC):
    @abstractmethod
    def use(self):
        pass


class Combinable(ABC):
    @abstractmethod
    def combine(self, item):
        pass


class Obtainable(ABC):
    @abstractmethod
    def take(self):
        pass


class Accessible(ABC):
    @abstractmethod
    def go(self):
        pass


class Examinable(ABC):
    @abstractmethod
    def examine(self):
        pass
