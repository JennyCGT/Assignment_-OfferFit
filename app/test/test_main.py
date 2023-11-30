
from fastapi import testclient
import pytest
from app.main import app

# client = testclient.TestClient(app)
@pytest.fixture
def test_client():
    # Set up a fresh TestClient for each test
    with testclient.TestClient(app) as client:
        yield client

data = [{"customer_id":  123, "event_type":  "email_click", "timestamp":  "2023-10-23T14:30:00", "email_id":  1234, "clicked_link":  "https://example.com/some-link"},
{"customer_id":  456, "event_type":  "email_open", "timestamp":  "2023-10-24T11:30:00", "email_id":  998},
{"customer_id":  456, "event_type":  "email_unsubscribe", "timestamp":  "2023-10-24T11:30:25", "email_id":  998},
{"customer_id":  123, "event_type":  "purchase", "timestamp":  "25-10-2023T15:33:00", "email_id":  1234, "product_id": 357, "amount":  49.99}
]

def test_get_data(test_client):
    for event in data:
        test_client.post("/event-subscription/hook",
        json = {"data": event}
        )

    customer_id = 123
    response = test_client.get(f"/all_events/{customer_id}")
    json_data = response.json()
    print(json_data)
    assert response.status_code == 200
    assert isinstance(json_data, list)
    assert len(json_data) == 2

def test_get_data_empty(test_client):
    for event in data:
        test_client.post("/event-subscription/hook",
        json = {"data": event}
        )

    customer_id = 2628
    response = test_client.get(f"/all_events/{customer_id}")
    json_data = response.json()
    print(json_data)
    assert response.status_code == 200
    assert isinstance(json_data, list)
    assert len(json_data) == 0

   
def test_hook_ok(test_client):
    response = test_client.post("/event-subscription/hook",
                        json = {"data": {"customer_id":  123, "event_type":  "purchase", "timestamp":  "25-10-2023T15:33:00", "email_id":  1234, "product_id": 357, "amount":  49.99}}
    )
    assert response.status_code == 200

def test_hook_event_different_event(test_client):
    response = test_client.post("/event-subscription/hook",
                        json = {"data": {"customer_id":  123, "event_type":  "no_event", "timestamp":  "25-10-2023T15:33:00", "email_id":  1234, "product_id": 357, "amount":  49.99}}
    )
    assert response.status_code == 422

def test_hook_event_different_customer(test_client):
    response = test_client.post("/event-subscription/hook",
                        json = {"data": {"customer_id":  'id', "event_type":  "no_event", "timestamp":  "25-10-2023T15:33:00", "email_id":  1234, "product_id": 357, "amount":  49.99}}
    )
    assert response.status_code == 422


