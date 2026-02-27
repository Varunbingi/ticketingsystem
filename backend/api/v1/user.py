from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
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
from utils.email import send_email
from datetime import date

logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/")
async def get_all_users(
    db: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    search: Optional[str] = Query(None, description="Search term for username, email, firstname, lastname"),
    sort_by: Optional[str] = Query("id", description="Field to sort by"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    is_client: Optional[bool] = Query(None, description="Filter by client users"),
    suspended: Optional[bool] = Query(None, description="Filter by suspended users")
):
    Manager = aliased(User)

    # Base query
    query = select(
        User.id,
        User.username,
        User.firstname,
        User.lastname,
        User.email,
        User.phone,
        User.designation,
        User.reporting_to_id,
        User.suspended,
        User.deleted,
        User.is_client,
        User.created_by_id,
        User.updated_by_id,
        User.created_at,
        User.modified_at,
        Manager.firstname.label('manager.firstname'),
        Manager.lastname.label('manager.lastname'),
        Manager.email.label('manager.email'),
    ).join(Manager, Manager.id == User.reporting_to_id, isouter=True).where(User.deleted == False)

    count_query = select(func.count()).select_from(User).where(User.deleted == False)

    # Search
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

    # Filters
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

    # Total count for pagination
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = [dict(u._mapping) for u in result.all()]

    return {"total": total, "skip": skip, "limit": limit, "users": users}

@user_router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id);
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user

@user_router.post('/create')
async def create_user(userrequest: CreateUserRequest, 
                      background_tasks: BackgroundTasks,
                      authuser: Annotated[dict, Depends(get_current_user)],
                       db: AsyncSession = Depends(get_async_session )):
    create_user_model = User(
        username =  userrequest.username,
        firstname = userrequest.firstname,
        lastname = userrequest.lastname,
        email = userrequest.email,
        phone = userrequest.phone,
        designation = userrequest.designation,
        department_id =userrequest.department_id,
        reporting_to_id = userrequest.reporting_to,
        suspended = userrequest.suspended,
        deleted = userrequest.deleted,
        is_client = userrequest.is_client,
        created_by_id = authuser["id"],
        updated_by_id = authuser["id"], 
        password = password_hash.hash(userrequest.password)
    )
    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)

    logger.info("User is created successfully")
    email_context = {
        "name": userrequest.firstname,
        "email": userrequest.email,
        "registration_date": date.today().strftime("%B %d, %Y")
    }
    background_tasks.add_task(
        send_email,
        subject="Welcome Aboard!",
        recipient_email=[userrequest.email],
        template_name="user_registration.html",
        context=email_context
    )

    return {
        'error': False,
        'message': '',
        'data': create_user_model
    }

@user_router.put('/{user_id}/update')
async def update_user(user_id: int, userrequest: UpdateUserRequest, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id);
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

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
    return {
        'error': False,
        'message': '',
        'data': user
    }

@user_router.delete('/{user_id}/delete')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id);
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    user.deleted = True
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        'error': False,
        'message': f"User '{user.username}' deleted",
        'data': []
    }

@user_router.patch('/{user_id}/update-password')
async def update_password(user_id:int, userrequest: UpdatePasswordRequest, authuser: Annotated[dict, Depends(get_current_user)], db:AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id);
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    user.password = password_hash.hash(userrequest.password)
    user.updated_by_id = authuser["id"]
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {
        'error': False,
        'message': f"User '{user.username}' password updated",
        'data': user
    }

