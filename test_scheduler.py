"""
Pytest Unit Tests for FocusFlow Scheduler API
Uses Flask's built-in test client — no running server needed.
"""

import pytest
from Scheduler_API import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_all_meetings(client):
    response = client.get('/all')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5


def test_next_meeting(client):
    response = client.get('/next')
    assert response.status_code == 200
    data = response.get_json()
    assert 'title' in data
    assert 'start' in data
    assert 'end' in data


def test_schedule_valid_meeting(client):
    response = client.post('/schedule', json={
        "title": "Test Meeting",
        "start": "06:00",
        "duration": 30
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Test Meeting"
    assert data['start'] == "06:00"
    assert data['end'] == "06:30"


def test_schedule_conflict(client):
    response = client.post('/schedule', json={
        "title": "Conflict Meeting",
        "start": "13:30",
        "duration": 60
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_schedule_invalid_time(client):
    response = client.post('/schedule', json={
        "title": "Bad Meeting",
        "start": "25:00",
        "duration": 30
    })
    assert response.status_code == 400


def test_schedule_missing_json(client):
    response = client.post('/schedule')
    assert response.status_code in (400, 415)


def test_complete_meeting(client):
    response = client.post('/complete')
    assert response.status_code == 200
    data = response.get_json()
    assert 'title' in data
