from unittest.mock import MagicMock
from app.services import UserService
import app.extensions as extensions

def test_sign_up(mock_supabase):
    """Test that UserService.sign_up calls Auth and DB correctly."""
    # 1. Mock the Auth Response
    mock_auth_response = MagicMock()
    mock_auth_response.user.id = "user-123"
    mock_auth_response.user.email = "test@example.com"
    
    # Setup the mock to return this response when sign_up is called
    mock_supabase.auth.sign_up.return_value = mock_auth_response

    # 2. Mock the DB Insert (Profile creation)
    # We just need to ensure it doesn't crash; the return value doesn't matter much here
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    # 3. Run the service
    user = UserService.sign_up("test@example.com", "password123", "Test User")

    # 4. Verify the result
    assert user.email == "test@example.com"
    
    # 5. Verify Supabase Auth was called
    mock_supabase.auth.sign_up.assert_called_once()
    
    # 6. Verify DB Table was called (to save the profile)
    mock_supabase.table.assert_called_with("users_profile")