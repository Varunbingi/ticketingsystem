from fastapi import APIRouter, Depends, HTTPException
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.clients.contract import Contract
from db.schemas.clients.contract import ContractModel
from sqlalchemy import select
from typing import Annotated
from repositories.auth import get_current_user
from datetime import datetime, date


contract_router = APIRouter(prefix='/contract', tags=['contract'])

@contract_router.get("/{client_id}")
async def get_all_contract(client_id: int, db: AsyncSession = Depends(get_async_session)):
    results = await db.execute(select(Contract).where(Contract.client_id == client_id))
    records = results.scalars().all()
    if records:
        return records
    else:
        return []
    
@contract_router.get("/{contract_id}")
async def get_contract(contract_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    record = result.scalars().one_or_none() 
    if record:
        return record
    else:
        return []
    
@contract_router.post("/")
async def add_contract(contract: ContractModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    data = contract.model_dump()
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    data['created_by_id'] = authuser['id']
    data['modified_by_id'] = authuser['id']
    dataobj = Contract(**data)
    db.add(dataobj)

    try:
        await db.commit()
        await db.refresh(dataobj)

        return dataobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@contract_router.put("/{contract_id}")
async def update_contract(contract_id: int, contract: ContractModel, authusr: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    now = datetime.now().replace(microsecond=0)
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    record = result.scalars().first()
    if record:
        record.startdate = contract.startdate
        record.enddate = contract.enddate
        record.hours = contract.hours
        record.frequency = contract.frequency
        record.status = contract.status
        record.startdate = contract.startdate
        record.modified_by_id = authusr['id']
        record.modified_at = now

        try:
            await db.commit()
            
            return record
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))

@contract_router.delete("/{contract_id}")
async def delete_contract(contract_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    record = result.scalars().first()
    if record:
        await db.delete(record)
        await db.commit()

        return "Deleted successfully"
    else:
        return "No Record Found"



