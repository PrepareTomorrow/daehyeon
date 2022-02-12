import pytest

from model.conn import create_engine_session, Base
from main import app, get_db

from fastapi.testclient import TestClient


engine, session = create_engine_session(test=True)
Base.metadata.create_all(bind=engine)

token = None


def override_get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def api():
    app.dependency_overrides[get_db] = override_get_db
    test_app = TestClient(app)
    return test_app


def test_ping(api):
    response = api.get('/ping')
    assert response.status_code == 200
    assert response.json()['message'] == 'pong'


def test_sign_up(api):
    first_user = {
        'name': 'test_client',
        'email': 'test_client@test.com',
        'password': 'z0109975',
        'profile': 'This is Test!'
    }
    response = api.put('/sign-up', json=first_user)
    assert response.status_code == 200, response.text

    second_user = {
        'name': 'test_client2',
        'email': 'test_client2@test.com',
        'password': 'z0109975',
        'profile': 'This is Test!'
    }
    response = api.put('/sign-up', json=second_user)
    assert response.status_code == 200, response.text

    integrity_case = {
        'name': 'test_client',
        'email': 'test_client@test.com',
        'password': 'z0109975',
        'profile': 'This is Test!'
    }
    response = api.put('/sign-up', json=integrity_case)
    assert response.status_code == 400, response.text


def test_login(api):
    global token

    data = {
        'email': 'test_client@test.com',
        'password': 'z0109975'
    }
    response = api.post('/login', json=data)
    assert response.status_code == 200, response.text

    token = response.json()['access_token']

    no_user_case = {
        'email': 'no_user@test.com',
        'password': 'nouser'
    }
    response = api.post('/login', json=no_user_case)
    assert response.status_code == 400, response.text

    wrong_case = {
        'email': 'test_client@test.com',
        'password': 'q0101010'
    }
    response = api.post('/login', json=wrong_case)
    assert response.status_code == 400, response.text


def test_follow(api):
    data = {'user_id_to_follow': 2}
    response = api.put('/follow',
                       headers={'Authorization': token},
                       json=data)
    assert response.status_code == 200, response.text


def test_unfollow(api):
    data = {'user_id_to_follow': 2}
    response = api.put('/follow',
                       headers={'Authorization': token},
                       json=data)
    assert response.status_code == 200, response.text


def test_timeline(api):
    response = api.get('/timeline', headers={'Authorization': token})
    assert response.status_code == 200, response.text
