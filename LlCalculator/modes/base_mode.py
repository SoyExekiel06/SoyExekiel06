"""Base class for calculator modes."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseMode(ABC):
    """Abstract base class for all calculator modes."""

    def __init__(self, name: str, engine):
        self.name = name
        self.engine = engine
        self.memory: float = 0.0
        self.has_memory = False

    @abstractmethod
    def evaluate(self, expression: str) -> str:
        """Evaluate an expression and return result string."""
        pass

    @abstractmethod
    def get_buttons(self) -> list:
        """Return button layout configuration."""
        pass

    def memory_clear(self):
        self.memory = 0.0
        self.has_memory = False

    def memory_recall(self) -> str:
        return str(self.memory)

    def memory_store(self, value: float):
        self.memory = value
        self.has_memory = True

    def memory_add(self, value: float):
        self.memory += value
        self.has_memory = True

    def memory_subtract(self, value: float):
        self.memory -= value
        self.has_memory = True
