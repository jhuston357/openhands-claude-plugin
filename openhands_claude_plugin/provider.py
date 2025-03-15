"""Claude direct provider implementation."""

import json
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Union

import requests
from requests.cookies import RequestsCookieJar

logger = logging.getLogger(__name__)

class ClaudeDirectProvider:
    """Provider for direct integration with Anthropic's Claude models."""

    def __init__(
        self,
        session_key: Optional[str] = None,
        model: str = "claude-3-opus-20240229",
        timeout: int = 120,
    ):
        """Initialize the Claude direct provider.

        Args:
            session_key: Anthropic session key
            model: Claude model to use
            timeout: Request timeout in seconds
        """
        self.session_key = session_key
        self.model = model
        self.timeout = timeout
        self.session = requests.Session()
        self.cookies = RequestsCookieJar()
        
        if session_key:
            self.set_session_key(session_key)

    def set_session_key(self, session_key: str) -> None:
        """Set the session key for authentication.

        Args:
            session_key: Anthropic session key
        """
        self.session_key = session_key
        self.cookies.set("sessionKey", session_key)
        self.session.cookies = self.cookies

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """Generate a response from Claude.

        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stop_sequences: Sequences that stop generation

        Returns:
            Generated text response
        """
        if not self.session_key:
            raise ValueError("Session key is required. Use set_session_key() to set it.")

        conversation_id = str(uuid.uuid4())
        
        # Prepare the message payload
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        payload = {
            "conversation_uuid": conversation_id,
            "messages": messages,
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences
        
        # Make the request to Claude's direct endpoint
        try:
            response = self.session.post(
                "https://claude.ai/api/chat",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            if "content" in result and isinstance(result["content"], list):
                # Extract text content from the response
                text_content = "".join(
                    item["text"] for item in result["content"] 
                    if item.get("type") == "text" and "text" in item
                )
                return text_content
            
            # Fallback if the response format is different
            return json.dumps(result)
            
        except requests.RequestException as e:
            logger.error(f"Error communicating with Claude: {e}")
            raise

    def stream_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stop_sequences: Optional[List[str]] = None,
    ):
        """Stream a response from Claude.

        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stop_sequences: Sequences that stop generation

        Yields:
            Generated text chunks
        """
        if not self.session_key:
            raise ValueError("Session key is required. Use set_session_key() to set it.")

        conversation_id = str(uuid.uuid4())
        
        # Prepare the message payload
        messages = [{"role": "user", "content": prompt}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        payload = {
            "conversation_uuid": conversation_id,
            "messages": messages,
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        
        if stop_sequences:
            payload["stop_sequences"] = stop_sequences
        
        # Make the streaming request to Claude's direct endpoint
        try:
            response = self.session.post(
                "https://claude.ai/api/chat_stream",
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()
            
            # Process the streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        # Parse the SSE data
                        if line.startswith(b"data: "):
                            data = json.loads(line[6:].decode("utf-8"))
                            if "completion" in data:
                                yield data["completion"]
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse streaming response: {line}")
                        
        except requests.RequestException as e:
            logger.error(f"Error streaming from Claude: {e}")
            raise