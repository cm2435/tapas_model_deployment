from typing import List, Optional, Union, Dict, Tuple

from pydantic import BaseModel


class QAResponseSchema(BaseModel):
    predicted_answer_coordinates: List[List[tuple]]
    predicted_aggregation_indices: List[int]
