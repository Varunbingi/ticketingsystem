from pydantic import BaseModel
from typing import Optional

class RoleModel(BaseModel):
    name: str
    shortname: str
    description: Optional[str]

class RoleUserModel(BaseModel):
    userid: int
    roleid: int
