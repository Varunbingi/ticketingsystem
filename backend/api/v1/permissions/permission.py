from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from typing import Annotated
from db.models.permission import  Permission
from db.schemas.permission import PermissionModel, PermissionModel
from repositories.auth import get_current_user
from datetime import datetime, date
from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning



permission_router = APIRouter(prefix='/permission', tags=['permission'])

@permission_router.get("/")
async def get_all_permissions(request: Request,db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_all_permissions_route")

    try:
        new_span(request, "fetch_permissions_db")
        records = await db.execute(select(Permission))
        results = records.scalars().all()
        end_span(request)
        if results:
            log_info(request, f"Fetched {len(results)} permissions")
            return results
        else:
            log_warning(request, "No permissions found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching permissions: {str(exc)}")
        raise

    finally:
        end_span(request)

@permission_router.get('/{id}')
async def get_permission(request: Request,id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_permission_route")
    try:
        new_span(request, "fetch_permission_db")
        record = await db.execute(select(Permission).where(Permission.id == id))
        result = record.scalars().first()
        end_span(request)
        if result:
            log_info(request, f"Fetched permission {id}")
            return result
        else:
            log_warning(request, f"Permission {id} not found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching permission {id}: {str(exc)}")
        raise

    finally:
        end_span(request)

@permission_router.post("/")
async def add_permission(request:Request,permission: PermissionModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request,"add_permission_route")
    try:
        new_span(request, "prepare_permission_data")
        now = datetime.now().replace(microsecond=0)
        data = permission.model_dump()
        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data['created_by_id'] = authuser['id']
        data['modified_by_id'] = authuser['id']

        end_span(request)
        dataobj = Permission(**data)
        db.add(dataobj)
        new_span(request, "db_commit")
        try:
            await db.commit()
            await db.refresh(dataobj)
        
            log_info(request, f"Permission '{dataobj.name}' created successfully")
            return dataobj
           
        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Add permission route failed: {str(exc)}")
        raise

    finally:
        end_span(request)


@permission_router.put("/{id}")
async def update_permission(request: Request,id: int, category: PermissionModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request,"update_permission_route")
    try:
        now = datetime.now().replace(microsecond=0)
        new_span(request,"fetch_permission_db")
        record = await db.execute(select(Permission).where(Permission.id == id))
        result = record.scalars().first()
        end_span(request)
        if result:

            new_span(request, "update_permission_data")
            result.permission_category_id = category.permission_category_id
            result.name = category.name
            result.shortname = category.shortname
            result.description = category.description
            result.modified_by_id = authuser['id']
            result.modified_at = now

            end_span(request)

            new_span(request, "db_commit")

            try:
                await db.commit()
                await db.refresh(result)
                log_info(request, f"Permission {id} updated successfully")
                return result
            except Exception as exc:
                await db.rollback()
                log_exception(request, f"DB commit failed: {str(exc)}")
                raise HTTPException(status_code=400, detail=str(exc))
            finally:
                end_span(request)   
        else:
            log_warning(request, f"Permission {id} not found")
            return []
    except Exception as exc:
        log_exception(request, f"Update permission route failed: {str(exc)}")
        raise

    finally:
        end_span(request)
        
@permission_router.delete("/{id}")
async def delete_permisison(request: Request,id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "delete_permission_route")

    try:
        new_span(request,"fetch_permission_route")
        record = await db.execute(select(Permission).where(Permission.id == id))
        result = record.scalars().first()
        end_span(request)

        if result:
            new_span(request, "db_delete")
            await db.delete(result)
            await db.commit()

            end_span(request)

            log_info(request, f"Permission {id} deleted successfully")
            return "Deleted successfully"
        else:
            log_warning(request, f"Permission {id} not found")
            return "Permission not found"
    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete permission failed: {str(exc)}")
        raise

    finally:
        end_span(request)