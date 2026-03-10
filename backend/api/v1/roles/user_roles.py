from fastapi import APIRouter, HTTPException, Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_async_session
from db.models.role import RoleUser
from db.schemas.role import RoleUserModel
from sqlalchemy.future import select
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning



user_role_router = APIRouter(prefix="/userrole", tags=['userrole'])

@user_role_router.get("/")
async def get_all_roles(request: Request,db: AsyncSession = Depends(get_async_session)):
    try:
        new_span(request, "fetch_user_roles_db")

        records = await db.execute(select(RoleUser))
        results = records.scalars().all()

        end_span(request)

        if results:
            log_info(request, f"Fetched {len(results)} user roles")
            return results
        else:
            log_warning(request, "No user roles found")
            return "No User Roles Found"
    except Exception as exc:
        log_exception(request, f"Error fetching user roles: {str(exc)}")
        raise

    finally:
        end_span(request)
# @user_role_router.get("{id}")
# async def get_role(id: int, db: AsyncSession = Depends(get_async_session)):
#     records = await db.execute(select(RoleUser))
#     results = records.scalars().first()

#     if results:
#         return results
#     else:
#         return "No Roles Found"
    
@user_role_router.put("/")
async def add_role(request: Request,role: RoleUserModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request, "assign_role_route")

    try:
        new_span(request, "prepare_role_user_data")

        now = datetime.now().replace(microsecond=0)
        data = role.model_dump()

        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data["created_by_id"] = authuser["id"]
        data["modified_by_id"] = authuser["id"]

        end_span(request)

        dataobj = RoleUser(**data)
        db.add(dataobj)

        new_span(request, "db_commit")

        try:
            await db.commit()
            await db.refresh(dataobj)

            log_info(request, f"Role assigned to user successfully (role_id={dataobj.role_id}, user_id={dataobj.user_id})")
            return dataobj

        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Assign role route failed: {str(exc)}")
        raise
    finally:
        end_span(request)
@user_role_router.delete("/{id}")
async def delete_role(request: Request, id: int, db: AsyncSession = Depends(get_async_session)):

    new_span(request, "delete_user_role_route")

    try:
        new_span(request, "fetch_user_role_db")

        record = await db.execute(select(RoleUser).where(RoleUser.id == id))
        result = record.scalars().first()

        end_span(request)

        if result:

            new_span(request, "db_delete")

            await db.delete(result)
            await db.commit()

            end_span(request)

            log_info(request, f"User role {id} deleted successfully")
            return "Deleted successfully"

        else:
            log_warning(request, f"User role {id} not found")
            return "User Role not found"

    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete user role failed: {str(exc)}")
        raise

    finally:
        end_span(request)
