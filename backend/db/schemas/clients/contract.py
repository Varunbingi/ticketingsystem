from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContractModel(BaseModel):
    client_id: int
    startdate: date
    enddate: date
    hours: int
    frequency: int
    status: Optional[bool] = True
