from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from typing import Annotated
from db.models.permission import PermissionCategory
from db.schemas.permission import PermissionCategoryModel
from repositories.auth import get_current_user
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

pc_router = APIRouter(prefix='/permissioncategory', tags=['permissioncategory'])

@pc_router.get("/")
async def get_all_permission_categories(db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(PermissionCategory))
    results = records.scalars().all()

    if results:
        return results
    else:
        return []

# @pc_router.get('/{id}')
# async def get_permission_category(id: int, db: AsyncSession = Depends(get_async_session)):
#     record = await db.execute(select(PermissionCategory).where(PermissionCategory.id == id))
#     result = record.scalars().first()

#     if result:
#         return result
#     else:
#         return "No Permission Category Found"

@pc_router.post("/")
async def add_permission_category(category: PermissionCategoryModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    data = category.model_dump()
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = PermissionCategory(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)
        logger.info("Permission category is created")

        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
    
# @pc_router.put("/{id}")
# async def update_permission_category(id: int, category: PermissionCategoryModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
#     now = datetime.now().replace(microsecond=0)
#     record = await db.execute(select(PermissionCategory).where(PermissionCategory.id == id))
#     result = record.scalars().first()
#     if result:
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
#         return "Permission not Found"
    
@pc_router.delete("/{id}")
async def delete_permisison_category(id: int, db: AsyncSession = Depends(get_async_session)):
    record = await db.execute(select(PermissionCategory).where(PermissionCategory.id == id))
    result = record.scalars().first()

    if result:
        await db.delete(result)
        await db.commit()

        return "Deleted successfully"
    else:
        return "Permission Category not found"
