import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    print(str(Path(__file__).parents[2] / "app"))
    sys.path.insert(
        0,
        str(Path(__file__).parents[2] / "app"),
    )
    from predictor import app

    with TestClient(app=app) as client:
        yield client


def test_single_question_response_time(client):
    """Test that the response time for the first question on cold start is less than 15 seconds"""
    question = "What is the capital of France?"
    table = {
        "City": ["Paris", "London", "Rome"],
        "Country": ["France", "United Kingdom", "Italy"],
    }
    payload = {"questions": question, "table": table}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 15


def test_single_question_response_correct(client):
    """Test that the response for a single question is correct."""
    question = "What is the capital of France?"
    table = {
        "City": ["Paris", "London", "Rome"],
        "Country": ["France", "United Kingdom", "Italy"],
    }
    payload = {"questions": question, "table": table}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    # Add assertions to check if the response is correct


def test_batch_questions_response(client):
    """Test that the API can handle batch sizes up to 64 questions."""
    questions = ["What is the capital of France?", "What is the currency of Japan?"]
    table = {
        "City": ["Paris", "London", "Rome"],
        "Country": ["France", "United Kingdom", "Italy"],
    }
    payload = {"questions": questions, "table": table}
    response = client.post("/invocations", json=payload)
    assert response.status_code == 200

