from app.services import UserService
from app.extensions import supabase

def test_create_user(mock_supabase):
    """Test that UserService calls Supabase correctly."""
    # Setup the mock to return fake data
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
        {"id": "123", "email": "test@example.com", "name": "Test"}
    ]

    # Run the service
    user = UserService.create_user("test@example.com", "Test")

    # Verify the result
    assert user["email"] == "test@example.com"
    
    # Verify Supabase was called with correct arguments
    mock_supabase.table.assert_called_with("users_profile")