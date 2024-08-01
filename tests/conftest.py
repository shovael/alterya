from src.main import app
import pytest


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()
