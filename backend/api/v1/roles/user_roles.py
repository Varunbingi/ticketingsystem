from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.role import RoleUser
from db.schemas.role import RoleUserModel
from sqlalchemy.future import select
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

user_role_router = APIRouter(prefix="/userrole", tags=['userrole'])

@user_role_router.get("/")
async def get_all_roles(db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(RoleUser))
    results = records.scalars().all()

    if results:
        return results
    else:
        return "No User Roles Found"

# @user_role_router.get("{id}")
# async def get_role(id: int, db: AsyncSession = Depends(get_async_session)):
#     records = await db.execute(select(RoleUser))
#     results = records.scalars().first()

#     if results:
#         return results
#     else:
#         return "No Roles Found"
    
@user_role_router.put("/")
async def add_role(role: RoleUserModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    data = role.model_dump()
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = RoleUser(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)
        logger.info("Role is assigned")

        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@user_role_router.delete("/{id}")
async def delete_role(id: int, db: AsyncSession = Depends(get_async_session)):
    record = await db.execute(select(RoleUser).where(RoleUser.id == id))
    result = record.scalars().first()

    if result:
        await db.delete(result)
        await db.commit()

        return "Deleted successfully"
    else:
        return "User Role not found"
