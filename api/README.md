# REST API example application
This is the documatic implimentation of the API for doing Table QA with a finetuned TAPAS model. 

App is run by a websocket that launches async fastapi workers on a guicorn webserver.



## Example schema
    {
    "questions":[
        "Who is brad pitt?"
    ],
    "table":{
        "Actors":[
            "Brad Pitt",
            "Leonardo Di Caprio",
            "George Clooney"
        ],
        "Number of movies":[
            "87",
            "53",
            "69"
        ]
    }
    }
Multiple questions can be passed to allow for batch processing. Since the webserver is balanced with nginx the upstream timeout has been manually set to 15 mins,
but large batchsizes should be handled and split client side before being sent over to mitigate risks of the server running out of memory. 

## Expected Response 
    [
    {
        "question": "Who is brad pitt? ",
        "answer": "Brad Pitt",
        "predicted_aggregation": "NONE"
    }
    ]

Responses are batched whilst preserving sending order to minimise overhead.










