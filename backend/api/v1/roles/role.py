from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.role import Role
from db.schemas.role import RoleModel
from sqlalchemy.future import select
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

role_router = APIRouter(prefix="/role", tags=['role'])

@role_router.get("/")
async def get_all_roles(db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Role))
    results = records.scalars().all()

    if results:
        return results         
    else:
        return []

@role_router.get("/{id}")
async def get_role(id: int, db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Role))
    results = records.scalars().first()

    if results:
        return results
    else:
        return []
    
@role_router.post("/")
async def add_role(role: RoleModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    data = role.model_dump()
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = Role(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)
        logger.info("Role is created")

        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@role_router.delete("/{id}")
async def delete_role(id: int, db: AsyncSession = Depends(get_async_session)):
    record = await db.execute(select(Role).where(Role.id == id))
    result = record.scalars().first()

    if result:
        await db.delete(result)
        await db.commit()

        return "Deleted successfully"
    else:
        return "Role not found"
