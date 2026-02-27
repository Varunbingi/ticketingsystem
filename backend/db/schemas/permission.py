from pydantic import BaseModel
from typing import Optional

class PermissionCategoryModel(BaseModel):
    name: str
    shortname: str

class PermissionModel(BaseModel):
    permission_category_id: int
    name: str
    shortname: str
    description: Optional[str]

class UserPermissionModel(BaseModel):
    permission_category_id: int
    permission_id: int
    userid: int