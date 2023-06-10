from typing import Dict, List, Optional, Union

from pydantic import BaseModel

##INPUT VALIDATION SCHEMAS


class QARequestSchema(BaseModel):
    questions: Union[List[str], str]
    table: Dict[str, List[str]]
