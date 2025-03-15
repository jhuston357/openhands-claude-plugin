"""Example usage of the OpenHands Claude plugin."""

import os
import sys
import logging

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openhands_claude_plugin import ClaudeDirectProvider

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    """Run the example."""
    # Get the session key from the environment
    session_key = os.environ.get("CLAUDE_SESSION_KEY")
    if not session_key:
        print("Please set the CLAUDE_SESSION_KEY environment variable")
        return

    # Initialize the provider
    provider = ClaudeDirectProvider(session_key=session_key)
    
    # Generate a response
    prompt = "Explain quantum computing in simple terms"
    print(f"Prompt: {prompt}")
    print("\nGenerating response...")
    
    response = provider.generate(
        prompt=prompt,
        system_prompt="You are a helpful AI assistant that explains complex topics in simple terms.",
        temperature=0.7,
        max_tokens=500,
    )
    
    print("\nResponse:")
    print(response)
    
    # Stream a response
    prompt = "Write a short poem about technology"
    print(f"\nPrompt: {prompt}")
    print("\nStreaming response...")
    
    for chunk in provider.stream_generate(
        prompt=prompt,
        system_prompt="You are a creative AI assistant that writes poetry.",
        temperature=0.9,
        max_tokens=200,
    ):
        print(chunk, end="", flush=True)
    
    print("\n\nDone!")

if __name__ == "__main__":
    main()