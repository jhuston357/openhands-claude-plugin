# OpenHands Claude Plugin

A plugin for OpenHands that allows direct integration with Anthropic's Claude models without using the API.

## Features

- Direct integration with Claude models
- Bypass API usage for certain use cases
- Seamless integration with OpenHands

## Installation

```bash
pip install openhands-claude-plugin
```

## Usage

```python
from openhands_claude_plugin import ClaudeDirectProvider

# Initialize the provider
provider = ClaudeDirectProvider()

# Use it with OpenHands
response = provider.generate("Tell me about quantum computing")
print(response)
```

## Configuration

The plugin supports the following configuration options:

- `session_key`: Your Anthropic session key (required)
- `model`: Claude model to use (default: "claude-3-opus-20240229")
- `timeout`: Request timeout in seconds (default: 120)

## License

MIT