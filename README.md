# OpenHands Claude Plugin

A plugin for OpenHands that allows direct integration with Anthropic's Claude models without using the API.

## Features

- Direct integration with Claude models through the claude.ai interface
- Bypass API usage for certain use cases
- Seamless integration with OpenHands
- Support for both synchronous and streaming responses
- Compatible with all Claude models available on claude.ai

## How It Works

This plugin works by directly interfacing with the claude.ai web interface instead of using the official API. It requires a valid session key from a logged-in Claude session.

**Important Note**: This is an unofficial integration and may break if Anthropic changes their interface. Use at your own risk and consider using the official API for production applications.

## Installation

```bash
pip install openhands-claude-plugin
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/jhuston357/openhands-claude-plugin.git
```

## Usage

### Basic Usage

```python
from openhands_claude_plugin import ClaudeDirectProvider

# Initialize the provider with your session key
provider = ClaudeDirectProvider(session_key="your_session_key_here")

# Generate a response
response = provider.generate(
    prompt="Tell me about quantum computing",
    system_prompt="You are a helpful AI assistant that explains complex topics in simple terms.",
    temperature=0.7,
    max_tokens=1000
)
print(response)
```

### Streaming Responses

```python
# Stream a response
for chunk in provider.stream_generate(
    prompt="Write a short story about AI",
    system_prompt="You are a creative AI assistant.",
    temperature=0.9
):
    print(chunk, end="", flush=True)
```

## Getting Your Session Key

To use this plugin, you need to obtain your Claude session key:

1. Log in to [claude.ai](https://claude.ai)
2. Open your browser's developer tools (F12 or right-click > Inspect)
3. Go to the Application/Storage tab
4. Look for Cookies > claude.ai
5. Find the cookie named `sessionKey` and copy its value

## Configuration

The plugin supports the following configuration options:

- `session_key`: Your Anthropic session key (required)
- `model`: Claude model to use (default: "claude-3-opus-20240229")
- `timeout`: Request timeout in seconds (default: 120)

## License

MIT