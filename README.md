# AI-Powered CLI Assistant

A modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini model, featuring an extensible tool system for function calling.

## Features

- 🤖 **AI-Powered Conversations**: Chat with GPT-4o-mini through a CLI interface
- 🛠️ **Extensible Tool System**: Modular tools that can be easily added and customized
- 🔧 **Built-in Tools**: Calculator, Web Search and Slot Machine
- 🔒 **Secure Configuration**: Environment-based API key management
- ⚡ **Async Support**: Modern async/await patterns for optimal performance

## Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Installation

#### Option 1: Using uv (Recommended)
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIDSCubed
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

3. **Install the project in editable mode**
   ```bash
   uv pip install -e .
   ```

#### Option 2: Using pip
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIDSCubed
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the project in editable mode**
   ```bash
   pip install -e .
   ```

#### Setup Environment Variables
4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the assistant**
   ```bash
   aidscubed
   # or
   python main.py
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000
```

## Usage

### Basic Commands

- **Chat**: Simply type your message and press Enter
- **Help**: `/help` - Show available commands and tools
- **Tools**: `/tools` - List all available tools
- **Clear**: `/clear` - Clear conversation history
- **Exit**: `/exit` or `/quit` - Exit the application

### Available Tools

#### Calculator
Evaluate mathematical expressions safely.

**Example**: "What is 15 * 23 + 7?"

#### Web Search
Search for information on the web.

**Example**: "Search for information about Python programming"

#### Slots Machine
A gambling game that allows the user to play a slots machine game.

**Example**: "I want to gamble 50 credits in the slot machines."

## Project Structure

```
AIDSCubed/
├── src/
│   └── aidscubed/
│       ├── __init__.py      # Package initialization
│       ├── cli.py           # Command-line interface
│       ├── config.py        # Configuration management
│       ├── core.py          # Core architecture
│       └── tools.py         # Tool implementations
├── main.py                  # Entry point
├── pyproject.toml          # Project configuration
├── env.example             # Environment template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Development

### Adding New Tools

1. **Create a new tool class** in `src/aidscubed/tools.py`:

```python
class MyTool:
    name = "my_tool"
    description = "Description of what this tool does"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "Description of parameter"
                        }
                    },
                    "required": ["param1"]
                }
            }
        }
    
    async def execute(self, param1: str) -> str:
        # Your tool logic here
        return f"Result: {param1}"
```

2. **Register the tool** in `src/aidscubed/cli.py`:

```python
registry.register(MyTool())
```

### Running Tests

```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio

# Run tests
pytest
```

### Code Quality

The project uses Ruff for linting and formatting:

```bash
# Install ruff
uv add --dev ruff

# Format code
ruff format

# Lint code
ruff check
```

## Architecture

### Core Components

- **Config**: Manages environment variables and configuration
- **ToolRegistry**: Dynamic tool discovery and registration
- **Assistant**: Main conversation manager with OpenAI integration
- **Tool Protocol**: Interface for implementing new tools

### Design Patterns

- **Registry Pattern**: For dynamic tool management
- **Protocol Classes**: For type-safe tool interfaces
- **Async/Await**: For non-blocking API calls
- **Dependency Injection**: For flexible configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for the GPT models
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [uv](https://github.com/astral-sh/uv) for fast Python package management
