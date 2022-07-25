import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def do_get(client, path):
    response = client.get(path)
    return response.status_code, str(response.data), response.get_json()
    pass

def test_sample(client):
    status_code, body, data = do_get(client, '/')
    assert status_code == 200
    assert 'welcome' in body
