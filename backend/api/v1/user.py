from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks,Request
from db.schemas import user
from notifications.dispatcher import emit_event
from db.models.user import User
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.user import CreateUserRequest, UpdateUserRequest, UpdatePasswordRequest
from pwdlib import PasswordHash
from sqlalchemy.future import select
from typing import Annotated, List, Optional
from sqlalchemy import func, or_, asc, desc
from sqlalchemy.orm import aliased
from repositories.auth import get_current_user
import logging
from datetime import date
from db.models.notifications import NotificationPreference
from logging_system.log_helper import log_info, log_warning, log_error, log_exception, new_span, end_span,extract_user_id

password_hash = PasswordHash.recommended()

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/")
async def get_all_users(request: Request,
    db: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for username, email, firstname, lastname"),
    sort_by: Optional[str] = Query("id", description="Field to sort by"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    is_client: Optional[bool] = Query(None, description="Filter by client users"),
    suspended: Optional[bool] = Query(None, description="Filter by suspended users"),
    authuser: dict = Depends(get_current_user)
):  
    
    # Set actor info in request.state
    request.state.user_id = authuser["id"]

    new_span(request, "get_all_users")


    try:
        # Nested span: Build SQL query

        new_span(request, "build_query")
        Manager = aliased(User)
        query = select(
            User.id, User.username, User.firstname, User.lastname, User.email, User.phone,
            User.designation, User.reporting_to_id, User.suspended, User.deleted, User.is_client,
            User.created_by_id, User.updated_by_id, User.created_at, User.modified_at,
            Manager.firstname.label('manager.firstname'),
            Manager.lastname.label('manager.lastname'),
            Manager.email.label('manager.email')
        ).join(Manager, Manager.id == User.reporting_to_id, isouter=True).where(User.deleted == False)

        count_query = select(func.count()).select_from(User).where(User.deleted == False)

        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.firstname.ilike(search_term),
                    User.lastname.ilike(search_term)
                )
            )
            count_query = count_query.where(
                or_(
                    User.username.ilike(search_term),
                    User.email.ilike(search_term),
                    User.firstname.ilike(search_term),
                    User.lastname.ilike(search_term)
                )
            )

        # Apply filters
        if is_client is not None:
            query = query.where(User.is_client == is_client)
            count_query = count_query.where(User.is_client == is_client)
        if suspended is not None:
            query = query.where(User.suspended == suspended)
            count_query = count_query.where(User.suspended == suspended)

        # Sorting
        sort_column = getattr(User, sort_by, User.id)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        end_span(request)  # end build_query span

        # Nested span: Execute DB

        new_span(request, "execute_db")
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        users = [dict(u._mapping) for u in result.all()]
        end_span(request)  # end execute_db span

        log_info(request, "Fetched all users successfully")
        return {"total": total, "skip": skip, "limit": limit, "users": users}

    except Exception as e:
        log_exception(request, f"Error fetching users: {str(e)}")
        raise

    finally:
        end_span(request)  # end top-level get_all_users span


@user_router.get("/{user_id}")
async def get_user(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    authuser: dict = Depends(get_current_user)
):
    request.state.user_id = authuser["id"]

    new_span(request, "get_user")  # Top-level span
    try:
        # Nested span: Fetch user from DB

        new_span(request, "fetch_user_db")
        user = await db.get(User, user_id)
        end_span(request)  # end fetch_user_db

        if not user:
            log_warning(request, f"User {user_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        log_info(request, f"Fetched user {user_id} successfully")
        return user

    except Exception as e:
        log_exception(request, f"Error fetching user {user_id}: {str(e)}")
        raise

    finally:
        end_span(request)  # end top-level get_user span

@user_router.post('/create')
async def create_user(
    request: Request,
    userrequest: CreateUserRequest,
    background_tasks: BackgroundTasks,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):

    # set actor info for logging
    request.state.user_id = authuser["id"]

    new_span(request, "create_user")

    try:
        # insert user
        new_span(request, "insert_user_db")

        create_user_model = User(
            username=userrequest.username,
            firstname=userrequest.firstname,
            lastname=userrequest.lastname,
            email=userrequest.email,
            phone=userrequest.phone,
            designation=userrequest.designation,
            department_id=userrequest.department_id,
            reporting_to_id=userrequest.reporting_to,
            suspended=userrequest.suspended,
            deleted=userrequest.deleted,
            is_client=userrequest.is_client,
            created_by_id=authuser["id"],
            updated_by_id=authuser["id"],
            password=password_hash.hash(userrequest.password)
        )

        db.add(create_user_model)
        await db.commit()
        await db.refresh(create_user_model)

        end_span(request)  # end insert_user_db

        # prepare email context
        email_context = {
            "name": create_user_model.firstname,
            "email": create_user_model.email,
            "registration_date": date.today().strftime("%B %d, %Y")
        }

        # store notification preferences
        prefs = NotificationPreference(
            user_id=create_user_model.id,
            email_enabled=True,
            inapp_enabled=True
        )
        db.add(prefs)

        # send welcome event in background
        new_span(request, "send_notifications")

        background_tasks.add_task(
            emit_event,
            event_name="WELCOME",
            strategy="DIRECT",
            payload={
                "user_id": create_user_model.id,
                "message": f"Welcome {email_context['name']}! Your account is ready.",
                "email_context": email_context
            }
        )

        await db.commit()

        end_span(request)

        log_info(request, f"User '{create_user_model.username}' created successfully")

        return {
            "error": False,
            "message": "user_created",
            "data": create_user_model
        }

    except Exception as e:
        log_exception(request, f"Error creating user: {str(e)}")
        raise

    finally:
        end_span(request)  # end top-level create_user span


@user_router.put('/{user_id}/update')
async def update_user(request: Request,user_id: int, userrequest: UpdateUserRequest, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    

    # Set actor info for logging
    request.state.user_id = authuser["id"]

    new_span(request, "update_user")  # Top-level span
    try:
        # Nested span: Fetch user from DB
        new_span(request, "fetch_user_db")
        user = await db.get(User, user_id)
        end_span(request)  # end fetch_user_db

        if not user:
            log_warning(request, f"User {user_id} not found for update")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


        # Nested span: Update user DB
        new_span(request, "update_user_db")
        # Update only the fields that are provided
        for field, value in userrequest.dict(exclude_unset=True).items():
            if field == "password":
                setattr(user, field, password_hash.hash(value))
            else:
                setattr(user, field, value)

        user.updated_by_id = authuser["id"];
        db.add(user)
        await db.commit()
        await db.refresh(user)
        end_span(request)  # end update_user_db
        log_info(request, f"User {user_id} updated successfully")
        return {
            'error': False,
            'message': '',
            'data': user
        }
    except Exception as e:
        log_exception(request, f"Error updating user {user_id}: {str(e)}")
        raise

    finally:
        end_span(request)  # end top-level update_user span

@user_router.delete('/{user_id}/delete')
async def delete_user(request: Request,user_id: int,authuser: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    
    # Set actor info for logging
    request.state.user_id = authuser["id"]

    
    
    new_span(request, "delete_user")  # Top-level span
    try:
        # Nested span: Fetch user from DB
        new_span(request, "fetch_user_db")
        user = await db.get(User, user_id)
        end_span(request)  # end fetch_user_db

        if not user:
            log_warning(request, f"User {user_id} not found for deletion")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        # Nested span: Mark user as deleted
        new_span(request, "delete_user_db")
        user.deleted = True
        db.add(user)
        await db.commit()
        await db.refresh(user)
        end_span(request)  # end delete_user_db

        log_info(request, f"User '{user.username}' deleted successfully")
        return {
            "error": False, 
            "message": f"User '{user.username}' deleted",
            "data": []}

    except Exception as e:
        log_exception(request, f"Error deleting user {user_id}: {str(e)}")
        raise

    finally:
        end_span(request)  # end top-level delete_user span


@user_router.patch('/{user_id}/update-password')
async def update_password(
    request: Request,
    user_id: int,
    userrequest: UpdatePasswordRequest,
    background_tasks: BackgroundTasks,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):

    # set actor info for logging
    request.state.user_id = authuser["id"]

    new_span(request, "update_password")

    try:
        # fetch user
        new_span(request, "fetch_user_db")

        user = await db.get(User, user_id)

        end_span(request)

        if not user or user.deleted:
            log_warning(request, f"User {user_id} not found or deleted")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )

        # update password
        new_span(request, "update_password_db")

        user.password = password_hash.hash(userrequest.password)
        user.updated_by_id = authuser["id"]

        db.add(user)
        await db.commit()
        await db.refresh(user)

        end_span(request)

        # emit security alert in background
        new_span(request, "emit_security_alert")

        background_tasks.add_task(
            emit_event,
            event_name="SECURITY_ALERT",
            strategy="DIRECT",
            payload={
                "user_id": user.id,
                "message": "Your account password was recently changed. If this wasn't you, contact support."
            }
        )

        end_span(request)

        log_info(request, f"User '{user.username}' password updated successfully")

        return {
            "error": False,
            "message": f"User '{user.username}' password updated",
            "data": user
        }

    except Exception as e:
        log_exception(request, f"Error updating password for user {user_id}: {str(e)}")
        raise

    finally:
        end_span(request)