from app import create_app

def test_config():
    """Test that testing config is loaded correctly."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing

def test_health_check():
    """Test the health check endpoint."""
    app = create_app({"TESTING": True})
    client = app.test_client()
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "message": "Friend is alive"}
