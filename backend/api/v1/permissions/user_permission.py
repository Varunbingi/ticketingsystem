from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from typing import Annotated
from db.models.permission import  UserPermission
from db.schemas.permission import UserPermissionModel
from repositories.auth import get_current_user
from datetime import datetime, date
from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning



up_router = APIRouter(prefix='/userpermission', tags=['userpermission'])

@up_router.get("/")
async def get_all_user_permissions(request: Request,db: AsyncSession = Depends(get_async_session)):
    
    new_span(request, "get_all_user_permissions_route")
    try:
        new_span(request, "fetch_user_permissions_db")
        records = await db.execute(select(UserPermission))
        results = records.scalars().all()

        end_span(request)
        if results:
            log_info(request, f"Fetched {len(results)} user permissions")

            return results
        else:
            log_warning(request, "No user permissions found")
            return "No Permissions Found"
    except Exception as exc:
        log_exception(request, f"Error fetching user permissions: {str(exc)}")
        raise

    finally:
        end_span(request)



# @up_router.get('/{id}')
# async def get_permission(id: int, db: AsyncSession = Depends(get_async_session)):
#     record = await db.execute(select(UserPermission).where(UserPermission.id == id))
#     result = record.scalars().first()

#     if result:
#         return result
#     else:
#         return "No Permission Found"

@up_router.post("/")
async def add_user_permission(request: Request,permission: UserPermissionModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request, "add_user_permission_route")
    try:
        new_span(request, "prepare_user_permission_data")
        now = datetime.now().replace(microsecond=0)
        data = permission.model_dump()
        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data['created_by_id'] = authuser['id']
        data['modified_by_id'] = authuser['id']
        end_span(request)
        dataobj = UserPermission(**data)
        db.add(dataobj)
        new_span(request, "db_commit")

        try:
            await db.commit()
            await db.refresh(dataobj)
            
            log_info(request, f"User permission created successfully (id={dataobj.id})")
            return dataobj
        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Add user permission route failed: {str(exc)}")
        raise

    finally:
        end_span(request)
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
async def delete_user_permisison(request:Request,id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request,"delete_user_permission_route")
    try: 
        new_span(request, "fetch_user_permission_db")  
        record = await db.execute(select(UserPermission).where(UserPermission.id == id))
        result = record.scalars().first()

        end_span(request)

        if result:

            new_span(request, "db_delete")

            await db.delete(result)
            await db.commit()
            end_span(request)

            log_info(request, f"User permission {id} deleted successfully")
            return "Deleted successfully"
        else:
            log_warning(request, f"User permission {id} not found")
            return "User Permission not found"
    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete user permission failed: {str(exc)}")
        raise
    finally:
        end_span(request)