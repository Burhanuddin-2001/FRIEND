from unittest.mock import patch, MagicMock
from app.services import AIService

@patch("app.services.requests.post")
def test_generate_message(mock_post):
    """Test that AIService calls Priyanshu API correctly."""
    # 1. Setup the mock response data
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "choices": [
                {
                    "message": {
                        "content": "Hey Tim, hope you are good!"
                    }
                }
            ]
        }
    }
    mock_post.return_value = mock_response

    # 2. Call the service
    result = AIService.generate_message("Tim")

    # 3. Verify result
    assert result == "Hey Tim, hope you are good!"

    # 4. Verify the API was called with correct URL
    args, kwargs = mock_post.call_args
    assert args[0] == "https://priyanshuapi.xyz/api/runner/priyanshu-ai"
    assert "Tim" in kwargs['json']['prompt']    