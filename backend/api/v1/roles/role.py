from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.role import Role
from db.schemas.role import RoleModel
from sqlalchemy.future import select
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning


role_router = APIRouter(prefix="/role", tags=['role'])

@role_router.get("/")
async def get_all_roles(request:Request,db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_all_roles_route")

    try:
        new_span(request, "fetch_roles_db")
        records = await db.execute(select(Role))
        results = records.scalars().all()
        end_span(request)

        if results:
            log_info(request, f"Fetched {len(results)} roles")
            return results         
        else:
            log_warning(request, "No roles found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching roles: {str(exc)}")
        raise

    finally:
        end_span(request)

@role_router.get("/{id}")
async def get_role(request:Request,id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_role_route")

    try:
        new_span(request, "fetch_role_db")

        records = await db.execute(select(Role).where(Role.id == id))
        result = records.scalars().first()

        end_span(request)

        if result:
            log_info(request, f"Fetched role {id}")
            return result
        else:
            log_warning(request, f"Role {id} not found")
            return []

    except Exception as exc:
        log_exception(request, f"Error fetching role {id}: {str(exc)}")
        raise

    finally:
        end_span(request)
    
@role_router.post("/")
async def add_role(request: Request,role: RoleModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request, "add_role_route")
    try:
        new_span(request, "prepare_role_data")
        now = datetime.now().replace(microsecond=0)
        data = role.model_dump()
        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data['created_by_id'] = authuser['id']
        data['modified_by_id'] = authuser['id']
        end_span(request)
        dataobj = Role(**data)
        db.add(dataobj)

        new_span(request, "db_commit")

        try:
            await db.commit()
            await db.refresh(dataobj)
            log_info(request, f"Role '{dataobj.name}' created successfully")
            return dataobj
        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Add role route failed: {str(exc)}")
        raise

    finally:
        end_span(request)

@role_router.delete("/{id}")
async def delete_role(request: Request, id: int, db: AsyncSession = Depends(get_async_session)):

    new_span(request, "delete_role_route")

    try:
        new_span(request, "fetch_role_db")

        record = await db.execute(select(Role).where(Role.id == id))
        result = record.scalars().first()

        end_span(request)

        if result:

            new_span(request, "db_delete")

            await db.delete(result)
            await db.commit()

            end_span(request)

            log_info(request, f"Role {id} deleted successfully")
            return "Deleted successfully"

        else:
            log_warning(request, f"Role {id} not found")
            return "Role not found"
        
    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete role failed: {str(exc)}")
        raise

    finally:
        end_span(request)