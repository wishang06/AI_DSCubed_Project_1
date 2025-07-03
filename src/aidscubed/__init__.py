"""AI-Powered CLI Assistant with extensible tool system."""

__version__ = "0.1.0"

from .cli import main
from .config import Config
from .core import Assistant, ToolRegistry
from .tools import Calculator, WebSearch, SlotMachine

__all__ = [
    "main",
    "Config", 
    "Assistant",
    "ToolRegistry",
    "Calculator",
    "WebSearch", 
    "SlotMachine",
] 