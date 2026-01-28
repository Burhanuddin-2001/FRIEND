from unittest.mock import MagicMock
import app.extensions as extensions

def test_home_page(client):
    """Test that the home page loads."""
    response = client.get("/")
    assert response.status_code == 200
    # Check for "Friend" instead of "Friend's Hand" to match your rename
    assert b"Friend" in response.data

def test_register_route_get(client):
    """Test that register page loads."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_register_post_success(client, mock_supabase):
    """Test registration logic."""
    # 1. Mock the Auth Sign Up response
    mock_user = MagicMock()
    mock_user.user.id = "user-123"
    mock_user.user.email = "test@example.com"
    
    # When auth.sign_up is called, return our mock user
    mock_supabase.auth.sign_up.return_value = mock_user

    # 2. Mock the DB Insert (Profile creation)
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    # 3. Perform the POST request
    response = client.post("/register", data={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }, follow_redirects=True)

    # 4. Assertions
    assert response.status_code == 200
    assert b"Registration successful" in response.data