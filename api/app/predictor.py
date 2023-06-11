from typing import Optional, Union

import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, Response
from schemas.input_schemas import QARequestSchema
from schemas.response_schemas import QAResponseSchema
from serving.model import InferenceModel

app = FastAPI()
controller = APIRouter()


@app.on_event("startup")
def startup_event():
    """Method to be called when the app starts up.

    - Downloads the wrapped class for fine-tuned Tapas models.
    """
    print("downloading wrapped class for models-")
    global model
    model = InferenceModel()


@controller.get("/ping")
def ping():
    """SageMaker required method, ping heartbeat"""
    return Response(status_code=200)


@controller.post(
    "/invocations",
    status_code=200,
)
async def transformation(schema: QARequestSchema):
    """Endpoint for performing the transformation.

    Args:
        schema: The request schema containing the questions and table.

    Returns:
        The response containing the predicted answer coordinates and aggregation indices.
    """
    response = model.inference(
        questions=schema.questions, table=pd.DataFrame.from_dict(schema.table)
    )
    return response


app.include_router(controller)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8002)
