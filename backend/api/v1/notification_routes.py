from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from db.models.notifications import NotificationPreference
from db.models.notifications import Notification
from repositories.auth import get_current_user
from typing import Annotated
from db.schemas.notifications import UpdatePreferenceRequest

notification_router = APIRouter(prefix="/notifications", tags=["notifications"])

@notification_router.get("/")
async def get_my_notifications(
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
    limit: int = 20
):
    """
    Fetches the latest in-app notifications for the logged-in user.
    """
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == authuser["id"])
        .order_by(Notification.created_at.desc())
        .limit(limit)
    )
    notifications = result.scalars().all()
    return notifications

@notification_router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    """
    Marks a specific notification as read so it stops highlighting in the UI.
    """
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, 
            Notification.user_id == authuser["id"]
        )
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    notification.read_status = True
    await db.commit()
    return {"status": "success", "message": "Notification marked as read"}

@notification_router.patch("/preferences")
async def update_preferences(
    request: UpdatePreferenceRequest,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    # 1. Find the user's existing preferences
    result = await db.execute(
        select(NotificationPreference).where(NotificationPreference.user_id == authuser["id"])
    )
    prefs = result.scalar_one_or_none()

    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")

    # 2. Update only the fields provided in the request
    if request.email_enabled is not None:
        prefs.email_enabled = request.email_enabled
    if request.sms_enabled is not None:
        prefs.sms_enabled = request.sms_enabled
    if request.inapp_enabled is not None:
        prefs.inapp_enabled = request.inapp_enabled

    await db.commit()
    return {"message": "Preferences updated successfully", "preferences": prefs}