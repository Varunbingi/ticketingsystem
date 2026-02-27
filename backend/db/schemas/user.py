from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field

class CreateUserRequest(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    email: str
    phone: str
    department_id: Optional[int] = None
    designation: str
    reporting_to: Optional[int] = None
    suspended: bool = False
    deleted: bool = False
    is_client: bool = False

class UpdateUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    phone: str
    designation: str
    reporting_to: Optional[int] = None
    suspended: bool = False
    deleted: bool = False
    is_client: bool = False

class UpdatePasswordRequest(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str