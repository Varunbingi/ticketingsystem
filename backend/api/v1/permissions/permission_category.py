from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from typing import Annotated
from db.models.permission import PermissionCategory
from db.schemas.permission import PermissionCategoryModel
from repositories.auth import get_current_user
from datetime import datetime, date

from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning



pc_router = APIRouter(prefix='/permissioncategory', tags=['permissioncategory'])

@pc_router.get("/")
async def get_all_permission_categories(request:Request,db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_all_permission_categories_route")
    try:
        new_span(request,"fetch_permission_categories_db")
        records = await db.execute(select(PermissionCategory))
        results = records.scalars().all()
        end_span(request)
        if results:
            log_info(request, f"Fetched {len(results)} permission categories")
            return results
        else:
            log_warning(request, "No permission categories found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching permission categories: {str(exc)}")
        raise
    finally:
        end_span(request)



# @pc_router.get('/{id}')
# async def get_permission_category(id: int, db: AsyncSession = Depends(get_async_session)):
#     record = await db.execute(select(PermissionCategory).where(PermissionCategory.id == id))
#     result = record.scalars().first()

#     if result:
#         return result
#     else:
#         return "No Permission Category Found"

@pc_router.post("/")
async def add_permission_category(request:Request,category: PermissionCategoryModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request,"add_permission_category_route")
    try:
        new_span(request, "prepare_permission_category_data")
        now = datetime.now().replace(microsecond=0)
        data = category.model_dump()
        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data['created_by_id'] = authuser['id']
        data['modified_by_id'] = authuser['id']
        end_span(request)  # prepare_permission_category_data
        dataobj = PermissionCategory(**data)
        db.add(dataobj)

        new_span(request, "db_commit")
        try:
            await db.commit()
            await db.refresh(dataobj)
            log_info(request, f"Permission category '{dataobj.name}' created successfully")
            return dataobj
        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)  # db_commit

    except Exception as exc:
        log_exception(request, f"Add permission category route failed: {str(exc)}")
        raise
    finally:
        end_span(request)
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
async def delete_permisison_category(request:Request,id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request,"delete_permission_category_route")    
    try:
        new_span(request,"fetch_permission_category_db")
        record = await db.execute(select(PermissionCategory).where(PermissionCategory.id == id))
        result = record.scalars().first()
        end_span(request)  # fetch_permission_category_db

        if result:
            new_span(request, "db_delete")
            await db.delete(result)
            await db.commit()
            end_span(request)  # db_delete

            log_info(request, f"Permission category {id} deleted successfully")
            return "Deleted successfully"

          
        else:
            log_warning(request, f"Permission category {id} not found")
            return "Permission Category not found"
        
    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete permission category failed: {str(exc)}")
        raise
    finally:
        end_span(request)