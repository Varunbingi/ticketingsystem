from fastapi import APIRouter, Depends, HTTPException
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.clients.client import Client
from sqlalchemy import select, desc
from db.schemas.clients.client import ClientModel
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
from notifications.dispatcher import emit_event

client_router = APIRouter(prefix="/clients", tags=["clients"])

@client_router.get("/")
async def get_all_clients(db: AsyncSession = Depends(get_async_session)):
    results = await db.execute(select(Client).order_by(desc(Client.id)))
    records = results.scalars().all()
    if records:
        return records
    else:
        return []

@client_router.get("/{id}")
async def get_client(id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Client).where(Client.id == id))
    record = result.scalars().first()
    if record:
        return record
    else:
        return []
    
@client_router.post("/")
async def add_client(client: ClientModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    data = client.model_dump()
    now = datetime.now().replace(microsecond=0)
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = Client(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)
        await emit_event(
            event_name="WELCOME", # Or "CLIENT_REGISTERED"
            strategy="DIRECT",
            payload={
                "user_id": authuser["id"], # Or the client's internal user ID if mapped
                "message": f"Client '{dataobj.name}' has been successfully registered."
        }
        )
        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
    
@client_router.put("/{client_id}")
async def update_client(client_id: int, client: ClientModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    result = await db.execute(select(Client).where(Client.id == client_id))
    record = result.scalars().one_or_none()
    if record:
        record.name = client.name
        record.email = client.email
        record.phone = client.phone
        record.address = client.address
        record.startdate = client.startdate
        record.enddate = client.enddate
        record.modified_at = now
        record.modified_by_id = authuser['id']
        
        try:
            await db.commit()
            await db.refresh(record)

            return record
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
    else:
        return "Client not Found"
    
@client_router.delete("/{client_id}")
async def delete_client(client_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Client).where(Client.id == client_id))
    record = result.scalars().one_or_none()
    if record:
        await db.delete(record)
        await db.commit()

        return "Deleted Successfully"
    else:
        return "Client not Found"