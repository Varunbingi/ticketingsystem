from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from typing import Annotated
from db.models.permission import  UserPermission
from db.schemas.permission import UserPermissionModel
from repositories.auth import get_current_user
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

up_router = APIRouter(prefix='/userpermission', tags=['userpermission'])

@up_router.get("/")
async def get_all_user_permissions(db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(UserPermission))
    results = records.scalars().all()

    if results:
        return results
    else:
        return "No Permissions Found"

# @up_router.get('/{id}')
# async def get_permission(id: int, db: AsyncSession = Depends(get_async_session)):
#     record = await db.execute(select(UserPermission).where(UserPermission.id == id))
#     result = record.scalars().first()

#     if result:
#         return result
#     else:
#         return "No Permission Found"

@up_router.post("/")
async def add_user_permission(permission: UserPermissionModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    data = permission.model_dump()
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = UserPermission(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)
        logger.info("User Permission is created")

        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
    
# @up_router.put("/{id}")
# async def update_permission(id: int, category: UserPermissionModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
#     now = datetime.now().replace(microsecond=0)
#     record = await db.execute(select(UserPermission).where(UserPermission.id == id))
#     result = record.scalars().first()
#     if result:
#         result.permission_category_id = category.permission_category_id
#         result.name = category.name
#         result.shortname = category.shortname
#         result.modified_by_id = authuser['id']
#         result.modified_at = now

#         try:
#             await db.commit()
#             await db.refresh(result)

#             return result
#         except Exception as exc:
#             await db.rollback()

#             raise HTTPException(status_code=400, detail=str(exc))
#     else:
#         return "User Permission not Found"
    
@up_router.delete("/{id}")
async def delete_user_permisison(id: int, db: AsyncSession = Depends(get_async_session)):
    record = await db.execute(select(UserPermission).where(UserPermission.id == id))
    result = record.scalars().first()

    if result:
        await db.delete(result)
        await db.commit()

        return "Deleted successfully"
    else:
        return "User Permission not found"
