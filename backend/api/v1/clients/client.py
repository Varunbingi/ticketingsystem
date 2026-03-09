
from fastapi import APIRouter, Depends, HTTPException , BackgroundTasks,Request

from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.clients.client import Client
from sqlalchemy import select, desc
from db.schemas.clients.client import ClientModel
from datetime import datetime
from typing import Annotated
from repositories.auth import get_current_user
from notifications.dispatcher import emit_event
from logging_system.log_helper import new_span, end_span, log_info, log_exception,log_warning

client_router = APIRouter(prefix="/clients", tags=["clients"])
background_tasks = BackgroundTasks()
@client_router.get("/")
async def get_all_clients(request:Request,db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_all_clients_route")
    try:
        new_span(request, "fetch_clients_db")
        results = await db.execute(select(Client).order_by(desc(Client.id)))
        records = results.scalars().all()
        end_span(request)  # fetch_clients_db

        if records:
            log_info(request, f"Fetched {len(records)} clients successfully")
            return records
        else:
            log_warning(request, "No clients found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching all clients: {str(exc)}")
        raise
    finally:
        end_span(request)  # get_all_clients_route

@client_router.get("/{id}")
async def get_client(request: Request, id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_client_route")
    try:
        new_span(request, "fetch_client_db")
        result = await db.execute(select(Client).where(Client.id == id))
        record = result.scalars().first()
        end_span(request)  # fetch_client_db

        if record:
            log_info(request, f"Fetched client {id} successfully")
            return record
        else:
            log_warning(request, f"Client {id} not found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching client {id}: {str(exc)}")
        raise
    finally:
        end_span(request)
    
@client_router.post("/")
async def add_client(
    request: Request,
    client: ClientModel,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "add_client_route")
    try:
        new_span(request, "prepare_client_data")

        data = client.model_dump()
        now = datetime.now().replace(microsecond=0)

        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data["created_by_id"] = authuser["id"]
        data["modified_by_id"] = authuser["id"]

        end_span(request)

        dataobj = Client(**data)
        db.add(dataobj)

        new_span(request, "db_commit")

        try:
            await db.commit()
            await db.refresh(dataobj)

            await emit_event(
                event_name="WELCOME",
                strategy="DIRECT",
                payload={
                    "user_id": authuser["id"],
                    "message": f"Client '{dataobj.name}' has been successfully registered."
                }
            )

            log_info(request, f"Client '{dataobj.name}' added successfully")
            return dataobj

        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))

        finally:
            end_span(request)

    except Exception as exc:
        log_exception(request, f"Add client route failed: {str(exc)}")
        raise

    finally:
        end_span(request)
        
@client_router.put("/{client_id}")
async def update_client(
    request: Request,
    client_id: int,
    client: ClientModel,
    authuser: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "update_client_route")

    try:
        now = datetime.now().replace(microsecond=0)

        new_span(request, "fetch_client_db")
        result = await db.execute(select(Client).where(Client.id == client_id))
        record = result.scalars().one_or_none()
        end_span(request)

        if record:
            new_span(request, "update_client_data")

            record.name = client.name
            record.email = client.email
            record.phone = client.phone
            record.address = client.address
            record.startdate = client.startdate
            record.enddate = client.enddate
            record.modified_at = now
            record.modified_by_id = authuser["id"]

            end_span(request)

            new_span(request, "db_commit")
            try:
                await db.commit()
                await db.refresh(record)

                log_info(request, f"Client {client_id} updated successfully")
                return record

            except Exception as exc:
                await db.rollback()
                log_exception(request, f"DB commit failed: {str(exc)}")
                raise HTTPException(status_code=400, detail=str(exc))

            finally:
                end_span(request)

        else:
            log_warning(request, f"Client {client_id} not found")
            raise HTTPException(status_code=404, detail="Client not found")

    except Exception as exc:
        log_exception(request, f"Update client route failed: {str(exc)}")
        raise

    finally:
        end_span(request)  # update_client_route
    
@client_router.delete("/{client_id}")
async def delete_client(request: Request, client_id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "delete_client_route")
    try:
        new_span(request, "fetch_client_db")
        result = await db.execute(select(Client).where(Client.id == client_id))
        record = result.scalars().one_or_none()
        end_span(request)  # fetch_client_db

        if record:
            new_span(request, "db_delete")
            await db.delete(record)
            await db.commit()
            end_span(request)  # db_delete

            log_info(request, f"Client {client_id} deleted successfully")
            return "Deleted Successfully"
        else:
            log_warning(request, f"Client {client_id} not found")
            return "Client not Found"
    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete client route failed: {str(exc)}")
        raise
    finally:
        end_span(request)  