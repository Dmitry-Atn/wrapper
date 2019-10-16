import pytest, io
from wrapper import *


@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        yield client


def test_predict_ok(client):
    data = {'file': (open("tests/res/image.jpg", "rb"), 'dress.jpg')}
    response = client.post(
        "/api/predict", data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'prediction' in response.data


def test_wrong_format(client):
    data = {'file': (io.BytesIO(b""), 'dress.jpg')}
    response = client.post(
        "/api/predict", data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'wrong attached file format' in response.data


def test_no_file_attached(client):
    data = {'file': ''}
    response = client.post(
        "/api/predict", data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'expected 1 file attached' in response.data


def test_file_not_found(client):
    data = {'attachment': (io.BytesIO(b""), 'dress.jpg')}
    response = client.post(
        "/api/predict", data=data,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'not found in request body' in response.data




