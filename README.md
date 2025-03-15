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

### Integration with OpenHands

To use this plugin with OpenHands, you'll need to register it as a provider in your OpenHands configuration:

```python
from openhands import OpenHands
from openhands_claude_plugin import ClaudeDirectProvider

# Initialize the Claude provider
claude_provider = ClaudeDirectProvider(
    session_key="your_session_key_here",
    model="claude-3-opus-20240229"
)

# Register the provider with OpenHands
openhands = OpenHands()
openhands.register_provider("claude-direct", claude_provider)

# Now you can use it in your OpenHands instance
response = openhands.generate(
    "Tell me about quantum computing",
    provider="claude-direct",
    system_prompt="You are a helpful AI assistant.",
    temperature=0.7
)
print(response)
```

#### Using in OpenHands Config File

You can also configure the provider in your OpenHands YAML configuration file:

```yaml
providers:
  claude-direct:
    type: custom
    module: openhands_claude_plugin
    class: ClaudeDirectProvider
    config:
      session_key: ${CLAUDE_SESSION_KEY}
      model: claude-3-opus-20240229
      timeout: 120

default_provider: claude-direct
```

Then in your code:

```python
from openhands import OpenHands

# OpenHands will load the Claude provider from your config
openhands = OpenHands.from_config("config.yaml")

# Use it directly
response = openhands.generate("Tell me about quantum computing")
print(response)
```

## Getting Your Session Key

To use this plugin, you need to obtain your Claude session key:

1. Log in to [claude.ai](https://claude.ai)
2. Open your browser's developer tools (F12 or right-click > Inspect)
3. Go to the Application/Storage tab
4. Look for Cookies > claude.ai
5. Find the cookie named `sessionKey` and copy its value

### Security Considerations

The session key provides full access to your Claude account. To use it securely:

1. Store it as an environment variable rather than hardcoding it:
   ```bash
   # Set the environment variable
   export CLAUDE_SESSION_KEY="your_session_key_here"
   ```

2. In your code, load it from the environment:
   ```python
   import os
   from openhands_claude_plugin import ClaudeDirectProvider
   
   # Load from environment variable
   session_key = os.environ.get("CLAUDE_SESSION_KEY")
   provider = ClaudeDirectProvider(session_key=session_key)
   ```

3. For OpenHands config files, use environment variable substitution:
   ```yaml
   providers:
     claude-direct:
       type: custom
       module: openhands_claude_plugin
       class: ClaudeDirectProvider
       config:
         session_key: ${CLAUDE_SESSION_KEY}
   ```

## Configuration

The plugin supports the following configuration options:

- `session_key`: Your Anthropic session key (required)
- `model`: Claude model to use (default: "claude-3-opus-20240229")
- `timeout`: Request timeout in seconds (default: 120)

## License

MIT