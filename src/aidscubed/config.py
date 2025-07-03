"""Configuration management for the AI CLI assistant."""

import os
from dataclasses import dataclass
from typing import Any
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class for the AI CLI assistant."""
    
    openai_api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        
        return cls(
            openai_api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000")),
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for OpenAI API."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        } 