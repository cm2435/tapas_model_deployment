from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel


class QAResponseSchema(BaseModel):
    predicted_answer_coordinates: List[List[tuple]]
    predicted_aggregation_indices: List[int]
