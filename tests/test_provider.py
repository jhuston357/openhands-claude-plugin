"""Tests for the Claude direct provider."""

import unittest
from unittest.mock import MagicMock, patch

from openhands_claude_plugin import ClaudeDirectProvider


class TestClaudeDirectProvider(unittest.TestCase):
    """Test cases for the Claude direct provider."""

    def setUp(self):
        """Set up the test case."""
        self.provider = ClaudeDirectProvider(session_key="test_key")

    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.provider.session_key, "test_key")
        self.assertEqual(self.provider.model, "claude-3-opus-20240229")
        self.assertEqual(self.provider.timeout, 120)

    @patch("requests.Session.post")
    def test_generate(self, mock_post):
        """Test generate method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [
                {"type": "text", "text": "This is a test response."}
            ]
        }
        mock_post.return_value = mock_response

        # Call the method
        response = self.provider.generate("Test prompt")

        # Check the result
        self.assertEqual(response, "This is a test response.")
        
        # Verify the request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "https://claude.ai/api/chat")
        self.assertEqual(kwargs["json"]["messages"][0]["role"], "user")
        self.assertEqual(kwargs["json"]["messages"][0]["content"], "Test prompt")
        self.assertEqual(kwargs["json"]["model"], "claude-3-opus-20240229")

    @patch("requests.Session.post")
    def test_generate_with_system_prompt(self, mock_post):
        """Test generate method with system prompt."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [
                {"type": "text", "text": "This is a test response."}
            ]
        }
        mock_post.return_value = mock_response

        # Call the method
        response = self.provider.generate(
            "Test prompt", system_prompt="You are a helpful assistant."
        )

        # Check the result
        self.assertEqual(response, "This is a test response.")
        
        # Verify the request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["messages"][0]["role"], "system")
        self.assertEqual(kwargs["json"]["messages"][0]["content"], "You are a helpful assistant.")
        self.assertEqual(kwargs["json"]["messages"][1]["role"], "user")
        self.assertEqual(kwargs["json"]["messages"][1]["content"], "Test prompt")

    def test_set_session_key(self):
        """Test set_session_key method."""
        provider = ClaudeDirectProvider()
        provider.set_session_key("new_key")
        self.assertEqual(provider.session_key, "new_key")
        self.assertEqual(provider.cookies.get("sessionKey"), "new_key")


if __name__ == "__main__":
    unittest.main()