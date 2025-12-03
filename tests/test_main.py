
import pytest
from unittest.mock import MagicMock, patch
from main import send_messages

def test_send_messages():
    # Create a mock response object
    mock_choice = MagicMock()
    mock_choice.message = "Mocked response"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    # Use patch to mock the OpenAI client's method
    with patch('main.client.chat.completions.create') as mock_create:
        mock_create.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        response = send_messages(messages)

        # Assert that the mocked method was called correctly
        mock_create.assert_called_once_with(
            model="deepseek-chat",
            messages=messages,
            tools=pytest.approx([
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get weather of a location, the user should supply a location first.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                }
                            },
                            "required": ["location"]
                        },
                    }
                },
            ])
        )

        # Assert that the function returns the expected message
        assert response == "Mocked response"

