import os
from typing import Dict, List
from abc import ABC, abstractmethod

class RunnableQueue(ABC):
    @abstractmethod
    def send(self, name, message):
        pass

    @abstractmethod
    def receive(self, name) -> str:
        pass