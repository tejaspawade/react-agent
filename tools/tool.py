from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    function: Callable
    parameters: dict

    def to_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def to_gemini_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }