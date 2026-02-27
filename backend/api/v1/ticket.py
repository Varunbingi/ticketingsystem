from fastapi import APIRouter, Depends, HTTPException,Form, File, UploadFile
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.ticket import ticketModel
from db.models.ticket import Ticket
from db.db import get_async_session
from typing import Annotated
from sqlalchemy.future import select
from repositories.auth import get_current_user
from datetime import datetime
import logging
import cloudinary.uploader


logger = logging.getLogger(__name__)

ticket_router = APIRouter(prefix="/ticket", tags=["ticket"])

@ticket_router.get('/')
async def list_of_tickets(db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Ticket))
    results = records.scalars().all()

    if results:
        return results         
    else:
        return []
    

@ticket_router.post("/")
async def create_ticket(
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),

    priority: int = Form(...),
    subject: str = Form(...),
    description: str | None = Form(None),
    files: List[UploadFile] = File(None),
):
    uploaded_urls = []
    if files:
        for file in files:
            upload = cloudinary.uploader.upload(
                file.file,
                folder="tickets",
                resource_type="auto"
            )
            uploaded_urls.append(upload["secure_url"])

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
    try:
        await db.commit()
        await db.refresh(ticket)
        logger.info("Ticket is created successfully")

        return ticket
         
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
   


@ticket_router.get('/{ticket_id}')
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    result = records.scalars().first()

    if result:
        return result         
    else:
        return []

@ticket_router.put("/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
    priority: int = Form(...),
    subject: str = Form(...),
    description: str | None = Form(None),
    files: List[UploadFile] = File(None),
):
    record = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = record.scalars().first()  
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    existing_files = list(ticket.files or [])

    if files:
        for file in files:
            upload = cloudinary.uploader.upload(
                file.file,
                folder="tickets",
                resource_type="auto"
            )
            existing_files.append(upload["secure_url"])
            
    ticket.priority = priority
    ticket.subject = subject
    ticket.files = existing_files
    ticket.status = 0
    ticket.description = description
    ticket.modified_by_id = authuser["id"]
    ticket.modified_at = datetime.now()
    print(ticket)
    db.add(ticket)
    try:
        await db.commit()
        await db.refresh(ticket)
        return ticket
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@ticket_router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    result = records.scalars().first()
    if result:
        try:
            await db.delete(result)
            await db.commit()
            return ticket_id
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
    else:
        return []

@ticket_router.get("/client/{client_id}")
async def get_tickets_by_clientId(client_id: int, db:AsyncSession = Depends(get_async_session)):
    records = await db.execute(select(Ticket).where(Ticket.client_id == client_id))
    print(records)
    result = records.scalars().all()
    print(result)
    if result:
        return result
    else:
        return []