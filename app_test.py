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
    #client = app.test_client()
    status_code, body, data = do_get(client, '/')
    #response = client.get('/')
    # GET /
    assert status_code == 200
    assert 'hello world!?' in body

    oldCount = data['count']

    status_code, body, data = do_get(client, '/')
    assert status_code == 200

    newCount = data['count']

    assert newCount == oldCount +  1

def test_abuse(client):
    status_code, body, data = do_get(client, '/')
    oldCount = data['count']
    assert status_code == 200

    status_code, _, _ = do_get(client, 'abuse')
    assert status_code == 200

    status_code, body, data = do_get(client, '/')
    newCount = data['count']

    assert newCount == oldCount + 100 + 1