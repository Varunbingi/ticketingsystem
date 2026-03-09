from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.db import get_async_session
from db.models.notifications import NotificationPreference
from db.models.notifications import Notification
from repositories.auth import get_current_user
from typing import Annotated
from db.schemas.notifications import UpdatePreferenceRequest
from logging_system.log_helper import new_span, end_span, log_info, log_warning, log_exception

notification_router = APIRouter(prefix="/notifications", tags=["notifications"])

@notification_router.get("/")
async def get_my_notifications(
    request: Request,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
    limit: int = 20
):
    """
    Fetches the latest in-app notifications for the logged-in user.
    """
    new_span(request, "get_my_notifications_route")

    try:
        new_span(request, "fetch_notifications_db")

        result = await db.execute(
            select(Notification)
            .where(Notification.user_id == authuser["id"])
            .order_by(Notification.created_at.desc())
            .limit(limit)
        )

        notifications = result.scalars().all()

        end_span(request)

        log_info(request, f"Fetched {len(notifications)} notifications for user {authuser['id']}")
        return notifications

    except Exception as exc:
        log_exception(request, f"Error fetching notifications: {str(exc)}")
        raise

    finally:
        end_span(request)

@notification_router.patch("/{notification_id}/read")
async def mark_as_read(
    request: Request,
    notification_id: int,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    """
    Marks a specific notification as read so it stops highlighting in the UI.
    """
    new_span(request, "mark_notification_read_route")

    try:
        new_span(request, "fetch_notification_db")

        result = await db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == authuser["id"]
            )
        )

        notification = result.scalar_one_or_none()

        end_span(request)

        if not notification:
            log_warning(request, f"Notification {notification_id} not found for user {authuser['id']}")
            raise HTTPException(status_code=404, detail="Notification not found")

        new_span(request, "update_notification_status")

        notification.read_status = True
        await db.commit()

        end_span(request)

        log_info(request, f"Notification {notification_id} marked as read")
        return {"status": "success", "message": "Notification marked as read"}

    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Error marking notification as read: {str(exc)}")
        raise

    finally:
        end_span(request)
@notification_router.patch("/preferences")
async def update_preferences(
    request: Request,
    body: UpdatePreferenceRequest,  # Request body containing preference changes
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update notification preferences (email, SMS, in-app).
    Only provided fields will be updated.
    """

    # Start route span
    new_span(request, "update_notification_preferences_route")

    try:
        # Start span for fetching existing preferences
        new_span(request, "fetch_preferences_db")

        # Query the user's notification preferences
        result = await db.execute(
            select(NotificationPreference)
            .where(NotificationPreference.user_id == authuser["id"])
        )

        prefs = result.scalar_one_or_none()

        # End DB fetch span
        end_span(request)

        # If preferences record does not exist
        if not prefs:
            log_warning(request, f"Notification preferences not found for user {authuser['id']}")
            raise HTTPException(status_code=404, detail="Preferences not found")

        # Start span for updating fields
        new_span(request, "update_preferences_data")

        # Update only the fields that were provided
        if body.email_enabled is not None:
            prefs.email_enabled = body.email_enabled

        if body.sms_enabled is not None:
            prefs.sms_enabled = body.sms_enabled

        if body.inapp_enabled is not None:
            prefs.inapp_enabled = body.inapp_enabled

        # Save updates
        await db.commit()

        # End update span
        end_span(request)

        # Log success
        log_info(request, f"Notification preferences updated for user {authuser['id']}")

        return {
            "message": "Preferences updated successfully",
            "preferences": prefs
        }

    except Exception as exc:
        # Rollback DB if update fails
        await db.rollback()

        # Log exception
        log_exception(request, f"Error updating preferences: {str(exc)}")
        raise

    finally:
        # Close route span
        end_span(request)