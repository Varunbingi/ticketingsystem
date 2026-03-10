
from fastapi import APIRouter, Depends, HTTPException,Form, File, UploadFile , BackgroundTasks,Request

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from notifications.dispatcher import emit_event
from db.schemas.ticket import ticketModel
from db.models.ticket import Ticket
from db.db import get_async_session
from typing import Annotated
from sqlalchemy.future import select
from repositories.auth import get_current_user
from datetime import datetime
import logging
import cloudinary.uploader
from logging_system.log_helper import new_span, end_span, log_info, log_warning, log_exception


ticket_router = APIRouter(prefix="/ticket", tags=["ticket"])

@ticket_router.get('/')
async def list_of_tickets(request:Request,db: AsyncSession = Depends(get_async_session)):
    new_span(request, "list_tickets_route")
    try: 
        new_span(request, "list_tickets_route")   
        records = await db.execute(select(Ticket))
        results = records.scalars().all()
        end_span(request)

        log_info(request, f"Fetched {len(results)} tickets")


        if results:
            return results         
        else:
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching tickets: {str(exc)}")
        raise

    finally:
        end_span(request)
        

@ticket_router.post("/")
async def create_ticket(
    request: Request,
    background_tasks: BackgroundTasks,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),

    priority: int = Form(...),
    subject: str = Form(...),
    description: str | None = Form(None),
    files: List[UploadFile] = File(None),
):
    new_span(request, "create_ticket_route")
    try:
        uploaded_urls = []

        # upload files to cloudinary
        if files:
            new_span(request, "upload_ticket_files")
            for file in files:
                upload = cloudinary.uploader.upload(
                    file.file,
                    folder="tickets",
                    resource_type="auto"
                )
                uploaded_urls.append(upload["secure_url"])

            log_info(request, f"{len(uploaded_urls)} files uploaded")
            end_span(request)

        now = datetime.now().replace(microsecond=0)

        ticket = Ticket(
            client_id=authuser["id"],
            priority=priority,
            subject=subject,
            description=description,
            files=uploaded_urls,
            status=0,
            created_by_id=authuser["id"],
            modified_by_id=authuser["id"],
            created_at=now,
            modified_at=now,
        )

        db.add(ticket)

        # commit ticket
        new_span(request, "db_commit_ticket")
        try:
            await db.commit()
            await db.refresh(ticket)

            log_info(request, f"Ticket created successfully id={ticket.id}")

        except Exception as exc:
            await db.rollback()
            log_exception(request, f"Ticket creation failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)

        # emit event in background
        new_span(request, "emit_ticket_created_event")
        try:
            background_tasks.add_task(
                emit_event,
                event_name="TICKET_CREATED",
                strategy="DIRECT",
                payload={
                    "user_id": authuser["id"],
                    "message": f"Your ticket regarding '{subject}' has been created."
                }
            )
        finally:
            end_span(request)

        return ticket

    except Exception as exc:
        log_exception(request, f"Create ticket route failed: {str(exc)}")
        raise

    finally:
        end_span(request)


@ticket_router.get('/{ticket_id}')
async def get_ticket(request: Request,ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_ticket_route")
    
    try:
        new_span(request, "fetch_ticket_db")

        records = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        result = records.scalars().first()

        end_span(request)

        if result:
            log_info(request, f"Fetched ticket {ticket_id}")
            return result

        log_warning(request, f"Ticket {ticket_id} not found")
        return []

    except Exception as exc:
        log_exception(request, f"Error fetching ticket {ticket_id}: {str(exc)}")
        raise

    finally:
        end_span(request)

@ticket_router.put("/{ticket_id}")
async def update_ticket(
    request:Request,
    ticket_id: int,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
    priority: int = Form(...),
    subject: str = Form(...),
    description: str | None = Form(None),
    files: List[UploadFile] = File(None),
):
    new_span(request, "update_ticket_route")

    try:
        new_span(request, "fetch_ticket_db")

        record = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = record.scalars().first()

        end_span(request)

        if not ticket:
            log_warning(request, f"Ticket {ticket_id} not found")
            raise HTTPException(status_code=404, detail="Ticket not found")

        existing_files = list(ticket.files or [])

        # Upload additional files
        if files:
            new_span(request, "upload_new_ticket_files")

            for file in files:
                upload = cloudinary.uploader.upload(
                    file.file,
                    folder="tickets",
                    resource_type="auto"
                )
                existing_files.append(upload["secure_url"])

            log_info(request, "New ticket files uploaded")

            end_span(request)

        # Update fields
        ticket.priority = priority
        ticket.subject = subject
        ticket.files = existing_files
        ticket.status = 0
        ticket.description = description
        ticket.modified_by_id = authuser["id"]
        ticket.modified_at = datetime.now()

        db.add(ticket)

        new_span(request, "db_commit_update")

        try:
            await db.commit()
            await db.refresh(ticket)

            log_info(request, f"Ticket {ticket_id} updated")

            # Emit notification event
            new_span(request, "emit_ticket_updated_event")

            await emit_event(
                event_name="TICKET_UPDATED",
                strategy="DIRECT",
                payload={
                    "user_id": authuser["id"],
                    "message": f"Ticket #{ticket_id} ('{subject}') has been updated."
                }
            )

            end_span(request)

            return ticket

        except Exception as exc:
            await db.rollback()
            log_exception(request, f"Ticket update failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))

        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Update ticket route failed: {str(exc)}")
        raise

    finally:
        end_span(request)

@ticket_router.delete("/{ticket_id}")
async def delete_ticket(request:Request,ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    
    new_span(request, "delete_ticket_route")

    try:
        new_span(request, "fetch_ticket_db")

        records = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        result = records.scalars().first()

        end_span(request)

        if not result:
            log_warning(request, f"Ticket {ticket_id} not found")
            return []

        new_span(request, "db_delete_ticket")

        await db.delete(result)
        await db.commit()

        end_span(request)

        log_info(request, f"Ticket {ticket_id} deleted")

        return ticket_id

    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete ticket failed: {str(exc)}")
        raise HTTPException(status_code=400, detail=str(exc))

    finally:
        end_span(request)

@ticket_router.get("/client/{client_id}")
async def get_tickets_by_clientId(request:Request,client_id: int, db:AsyncSession = Depends(get_async_session)):
    new_span(request, "get_client_tickets_route")

    try:
        new_span(request, "fetch_client_tickets_db")

        records = await db.execute(select(Ticket).where(Ticket.client_id == client_id))
        print(records)
        result = records.scalars().all()
        print(result)

        end_span(request)

        log_info(request, f"Fetched {len(result)} tickets for client {client_id}")

        return result if result else []

    except Exception as exc:
        log_exception(request, f"Error fetching client tickets: {str(exc)}")
        raise