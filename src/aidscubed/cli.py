"""Command-line interface for the AI CLI assistant."""

import asyncio
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from .config import Config
from .core import Assistant, ToolRegistry
from .tools import Calculator, WebSearch, SlotMachine


def display_banner() -> None:
    """Display the application banner."""
    console = Console()
    banner = Text()
    banner.append("🤖 ", style="bold blue")
    banner.append("AI-Powered CLI Assistant", style="bold green")
    banner.append(" v0.1.0", style="dim")
    
    console.print(Panel(banner, border_style="blue"))
    console.print()


def display_help() -> None:
    """Display help information."""
    console = Console()
    
    help_text = """
[bold]Available Commands:[/bold]
• Type your message to chat with the AI assistant
• [bold]/help[/bold] - Show this help message
• [bold]/tools[/bold] - List available tools
• [bold]/clear[/bold] - Clear conversation history
• [bold]/exit[/bold] or [bold]/quit[/bold] - Exit the application

[bold]Available Tools:[/bold]
• [bold]Calculator[/bold] - Evaluate mathematical expressions
• [bold]Web Search[/bold] - Search for current information using OpenAI's web search
• [bold]Slot Machine[/bold] - Play a virtual gambling game

[bold]Examples:[/bold]
• "What is 15 * 23 + 7?"
• "Search for information about Python programming"
• "Let's play the slot machine"
• "Spin the slot machine with 50 credits"
    """
    
    console.print(Panel(help_text, title="[blue]Help[/blue]", border_style="blue"))


def display_tools(registry: ToolRegistry) -> None:
    """Display available tools."""
    console = Console()
    
    table = Table(title="Available Tools")
    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    for tool in registry.get_all_tools():
        table.add_row(tool.name, tool.description)
    
    console.print(table)


async def main() -> None:
    """Main CLI entry point."""
    console = Console()
    
    try:
        # Load configuration
        config = Config.from_env()
        
        # Initialize tool registry
        registry = ToolRegistry()
        registry.register(Calculator())
        registry.register(WebSearch(config))
        registry.register(SlotMachine())
        
        # Initialize assistant
        assistant = Assistant(config, registry)
        
        # Display banner
        display_banner()
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[blue]You[/blue]")
                
                # Handle special commands
                if user_input.lower() in ["/exit", "/quit"]:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                elif user_input.lower() == "/help":
                    display_help()
                    continue
                elif user_input.lower() == "/tools":
                    display_tools(registry)
                    continue
                elif user_input.lower() == "/clear":
                    assistant.messages.clear()
                    console.print("[green]Conversation history cleared![/green]")
                    continue
                elif user_input.startswith("/"):
                    console.print(f"[red]Unknown command: {user_input}[/red]")
                    console.print("Type /help for available commands.")
                    continue
                
                # Display user message
                assistant.display_message("user", user_input)
                
                # Get assistant response
                with console.status("[dim]Thinking...[/dim]"):
                    response, tool_results = await assistant.chat(user_input)
                # Display tool results if any
                for tool_name, result in tool_results:
                    assistant.display_message("assistant", result, is_tool_call=True)
                # Display assistant response
                assistant.display_message("assistant", response)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
                continue
    
    except ValueError as e:
        console.print(f"[red]Configuration Error: {str(e)}[/red]")
        console.print("\n[bold]Setup Instructions:[/bold]")
        console.print("1. Create a .env file in the project root")
        console.print("2. Add your OpenAI API key:")
        console.print("3. Run the application again")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 