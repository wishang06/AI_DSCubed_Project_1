"""Core architecture for the AI CLI assistant."""

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, TypeAlias, Union
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .config import Config

# Type aliases for better readability
Message: TypeAlias = ChatCompletionMessageParam
ToolCall: TypeAlias = Dict[str, Any]
ToolResult: TypeAlias = Dict[str, Any]


class Tool(Protocol):
    """Protocol for tools that can be called by the assistant."""
    
    name: str
    description: str
    
    def get_schema(self) -> ChatCompletionToolParam:
        """Get the OpenAI function schema for this tool."""
        ...
    
    async def execute(self, *args: Any, **kwargs: Any) -> str:
        """Execute the tool with given parameters."""
        ...


class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool with the registry."""
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_schemas(self) -> List[ChatCompletionToolParam]:
        """Get OpenAI function schemas for all tools."""
        return [tool.get_schema() for tool in self._tools.values()]


class Assistant:
    """Main assistant class that manages conversation and tool execution."""
    
    def __init__(self, config: Config, registry: ToolRegistry) -> None:
        self.config = config
        self.registry = registry
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.console = Console()
        self.messages: List[Message] = []
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})  # type: ignore
    
    async def chat(self, user_input: str):
        """Process user input and return assistant response and tool results."""
        self.add_message("user", user_input)
        messages = self.messages.copy()
        tool_results = []
        if len(messages) == 1:
            system_msg = {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant with access to various tools. "
                    "Use the available tools when appropriate to help users. "
                    "Always provide clear, helpful responses."
                )
            }  # type: ignore
            messages.insert(0, system_msg)  # type: ignore
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                tools=self.registry.get_schemas(),
                tool_choice="auto",
                **self.config.to_dict(),
            )
            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    tool = self.registry.get_tool(tool_name)
                    if not tool:
                        result = f"Tool '{tool_name}' not found."
                    else:
                        try:
                            result = await tool.execute(**tool_args)
                        except Exception as e:
                            result = f"Error executing tool '{tool_name}': {str(e)}"
                    tool_results.append((tool_name, result))
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call.model_dump()],
                    })
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tool_call.id,
                    })
                
                response = await self.client.chat.completions.create(
                    messages=messages,
                    **self.config.to_dict(),
                )
                assistant_message = response.choices[0].message
            self.add_message("assistant", assistant_message.content or "")
            return assistant_message.content or "I apologize, but I couldn't generate a response.", tool_results
        except Exception as e:
            error_msg = f"Error communicating with OpenAI: {str(e)}"
            self.console.print(f"[red]{error_msg}[/red]")
            return error_msg, tool_results
    
    def display_message(self, role: str, content: str, is_tool_call: bool = False) -> None:
        """Display a message with appropriate styling."""
        if role == "user":
            self.console.print(Panel(content, title="[blue]You[/blue]", border_style="blue"))
        elif role == "assistant":
            if is_tool_call:
                self.console.print(Panel(content, title="[green]Tool Result[/green]", border_style="green"))
            else:
                self.console.print(Panel(content, title="[green]Assistant[/green]", border_style="green"))
        elif role == "system":
            self.console.print(Panel(content, title="[yellow]System[/yellow]", border_style="yellow")) 