# REST API example application
This is the documatic implimentation of our core code search API.

Impliments 3 main tasks:
1. smart_highlighting
2. embedding
3. keyword_generation

App is run by a websocket that launches async fastapi workers on a guicorn webserver.

`smart_highlighting` is the task to get a ranked list of the top lines for a given function that is returned
and their similarity scores to a given queries. 

`emebedding` is the task used to yield a List[List[float]] representing the embedding from our search models that 
can be piped to vespa to build indexes.

`keyword_generation` is the task used to yield a List[str] of keywords for a given query or block of code and their relative 
similarities 

## Install
    conda create --name <env_name> python==3.9 
    conda activate <env_name>
    pip install -r requirements.txt
    conda activate <env_name>

## Run the app

    python predictor.py 

## Run the tests

    pytest ./tests/

## Build and push the container to ECR 
    bash ./build_and_push.sh



## Example schema
    {
    "task": "embedding",
    "embedding_payload": {
        "code": [
        "def read_file(fp):\n\treturn pd.read_csv(fp)"
        ],
        "query": [
        "read file"
        ],
        "language": "python",
        "response_max_len": 64
    },
    "keyword_payload": {
        "code": [
        "def read_file(fp):\n\treturn pd.read_csv(fp)"
        ],
        "query": [
        "read file"
        ],
        "return_top_N": 20
    },
    "highlighting_payload": {
        "code": [
        "def read_file(fp):\n\treturn pd.read_csv(fp)"
        ],
        "query": "read file",
        "language": "python",
        "return_top_N": 20
    }
    }

    Only one task payload needs to be passed. For example, if task is embedding, only the embedding json field is needed.
















