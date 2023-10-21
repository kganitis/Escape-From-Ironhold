# properties.py
from abc import ABC, abstractmethod


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
