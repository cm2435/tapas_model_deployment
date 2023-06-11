import json 
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import numpy as np 

@pytest.fixture
def client():
    sys.path.insert(
        0,
        str(Path(__file__).parents[2] / "app"),
    )
    from predictor import app

    with TestClient(app=app) as client:
        yield client


@pytest.fixture
def data_dict():
    # Specify the path to your JSONLines file
    file_path = "testcases.jsonl"
    
    # Open the file and load its contents into a list of dictionaries
    with open(file_path, "r") as json_file:
        data_list = [json.loads(line) for line in json_file]
    return data_list


def test_api_responses(client, data_dict, min_accuracy : int = 0):
    correct_response_list = []
    for data in data_dict:
        data_request = {
            key: value
            for key, value in data.items()
            if key != "answers"
        }

        # Send a request to the API containing the data
        response = client.post("/invocations", json=data_request).json()[0]
        if response['answer'] == data['answers']:
            correct_response_list.append(1)
        else: 
            correct_response_list.append(0)
        
    #Check that it is greater than some threshold accuracy. Set to zero since having one example is fragile 
    assert np.average(correct_response_list) >= min_accuracy

