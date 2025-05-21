from enum import Enum
from typing import Optional


class ExampleStrategy(Enum):
    QUICKSTART = "quickstart"
    LANGGRAPH_AGENT = "langgraph_agent"

    @classmethod
    def from_string(cls, value: str) -> Optional["ExampleStrategy"]:
        """Convert a string to ExampleStrategy enum value"""
        for strategy in cls:
            if strategy.value == value.lower():
                return strategy
        return None
