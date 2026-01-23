import pytest
from unittest.mock import MagicMock
from app import create_app
import app.extensions as extensions_module

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # 1. Create a Mock Client
    mock_client = MagicMock()
    
    # 2. Inject the Mock into the extensions module
    # This replaces the 'None' or any previous client with our Mock
    extensions_module.supabase = mock_client
    
    # 3. Create the app (TESTING=True will prevent real init_supabase)
    application = create_app({"TESTING": True})
    
    yield application
    
    # 4. Cleanup: Reset to None after test
    extensions_module.supabase = None

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_supabase(app):
    """
    Helper to access the mock in tests.
    IMPORTANT: This fixture requests 'app' to ensure the app fixture runs first!
    """
    return extensions_module.supabase