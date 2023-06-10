from typing import List, Optional, Union, Dict
from typing import Dict, List
from pydantic import BaseModel

##INPUT VALIDATION SCHEMAS


class QARequestSchema(BaseModel):
    questions: Union[List[str], str]
    table: Dict[str, List[str]]
