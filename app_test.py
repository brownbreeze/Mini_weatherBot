import pytest
from app import app
import time

@pytest.fixture
def client():
    return app.test_client()

def do_get(client, path):
    response = client.get(path)
    return response.status_code, str(response.data), response.get_json()

def test_sample(client):
    status_code, body, data = do_get(client, '/')
    assert status_code == 200
    assert 'welcome' in body

def test_normal(client):
    status_code, body, data = do_get(client, '/summary?lat=13.3&lon=124')
    assert status_code == 200

def test_paramError(client):
    # wrong param
    status_code, body, data = do_get(client, '/summary?lat=3000&lon=124')
    assert status_code == 400

    # wrong param
    status_code, body, data = do_get(client, '/summary?lat=90&lon=180')
    assert status_code == 400

    # blank param
    status_code, body, data = do_get(client, '/summary?lon=124')
    assert status_code == 400

def test_timeout(client):
    for i in range(0, 10):
        start_time = time.process_time()
        status_code, body, data = do_get(client, '/summary?lat=13.3&lon=124')
        end_time = time.process_time()
        assert ((int(round((end_time - start_time) * 1000))) <= 1500 ) and ( status_code == 200 )

