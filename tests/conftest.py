import pytest
from flask import Flask
from Main import create_app

@pytest.fixture
def app():
    
    app = create_app({
        'TESTING': True
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
