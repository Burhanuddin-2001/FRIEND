from unittest.mock import patch, MagicMock
from app.services import EmailService

@patch("app.services.resend")
@patch("app.services.extensions.supabase") # Mock the DB logging too
def test_send_email(mock_supabase, mock_resend):
    """Test that EmailService calls Resend and logs to DB."""
    
    # 1. Setup Mocks
    mock_resend.Emails.send.return_value = {"id": "email_123"}
    mock_supabase.table.return_value.insert.return_value.execute.return_value = True

    # 2. Call Service
    success = EmailService.send_email(
        to_email="test@example.com",
        subject="Hello",
        body_html="<p>Hi</p>",
        user_id="user-123"
    )

    # 3. Assertions
    assert success is True
    
    # Check Resend was called
    mock_resend.Emails.send.assert_called_once()
    call_args = mock_resend.Emails.send.call_args[0][0]
    assert call_args["to"] == ["test@example.com"]
    assert call_args["subject"] == "Hello"

    # Check DB Logging was called
    mock_supabase.table.assert_called_with("email_logs")