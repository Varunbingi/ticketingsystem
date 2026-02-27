from pydantic import BaseModel
from datetime import date

class ClientModel(BaseModel):
    idnumber: int
    name: str
    email: str
    phone: str
    address: str
    startdate: date
    enddate: date