from fastapi import APIRouter, Depends, HTTPException, Request
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.clients.contract import Contract
from db.schemas.clients.contract import ContractModel
from sqlalchemy import select
from typing import Annotated
from repositories.auth import get_current_user
from datetime import datetime, date
from logging_system.log_helper import new_span, end_span, log_info, log_exception, log_warning



contract_router = APIRouter(prefix='/contract', tags=['contract'])

@contract_router.get("/{client_id}")
async def get_all_contract(request: Request,client_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        new_span(request, "fetch_contracts_db")
        results = await db.execute(select(Contract).where(Contract.client_id == client_id))
        records = results.scalars().all()
        end_span(request)
        if records:
            log_info(request, f"Fetched {len(records)} contracts of client {client_id}")
            return records
        else:
            log_warning(request, f"No contracts fond for client {client_id}")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching contracts: {str(exc)}")
        raise
    finally:
        end_span(request)  # get_all_contract_route

        
@contract_router.get("/{contract_id}")
async def get_contract(request:Request,contract_id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "get_contract_route")
    try:
        new_span(request, "fetch_contract_db")
        result = await db.execute(select(Contract).where(Contract.id == contract_id))
        record = result.scalars().one_or_none() 
        end_span(request)
        if record:
            log_info(request,f"Fetched contract {contract_id}")
            return record
        else:
            log_warning(request, f"Contract {contract_id} not found")
            return []
    except Exception as exc:
        log_exception(request, f"Error fetching contract {contract_id}: {str(exc)}")
        raise
    finally:
        end_span(request)
            
@contract_router.post("/")
async def add_contract(request:Request,contract: ContractModel, authuser: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request,"add_contract_route")
    try:
        new_span(request, "prepare_contract_data")
        now = datetime.now().replace(microsecond=0)
        data = contract.model_dump()
        data["created_at"] = data.get("created_at") or now
        data["modified_at"] = now
        data['created_by_id'] = authuser['id']
        data['modified_by_id'] = authuser['id']

        end_span(request)
        dataobj = Contract(**data)
        db.add(dataobj)

        new_span(request, "db_commit")

        try:
            await db.commit()
            await db.refresh(dataobj)

            log_info(request, f"Contract {dataobj.id} created successfully")
            return dataobj
        except Exception as exc:
            await db.rollback()
            log_exception(request, f"DB commit failed: {str(exc)}")
            raise HTTPException(status_code=400, detail=str(exc))
        finally:
            end_span(request)  # db_commit
    
    except Exception as exc:
        log_exception(request, f"Add contract route failed: {str(exc)}")
        raise
    finally:
        end_span(request)

@contract_router.put("/{contract_id}")
async def update_contract(request: Request,contract_id: int, contract: ContractModel, authusr: Annotated[dict, Depends(get_current_user)], db: AsyncSession = Depends(get_async_session)):
    new_span(request, "update_contract_ route")
    try:
        now = datetime.now().replace(microsecond=0)

        new_span(request, "fetch_contract_db")
        result = await db.execute(select(Contract).where(Contract.id == contract_id))
        record = result.scalars().first()
        end_span(request)  # fetch_contract_db
        if record:
            new_span(request, "update_contract_data")

            record.startdate = contract.startdate
            record.enddate = contract.enddate
            record.hours = contract.hours
            record.frequency = contract.frequency
            record.status = contract.status
            record.startdate = contract.startdate
            record.modified_by_id = authusr['id']
            record.modified_at = now

            end_span(request)  # update_contract_data

            new_span(request, "db_commit")
            try:
                await db.commit()
                await db.refresh(record)

                log_info(request, f"Contract {contract_id} updated successfully")
                
                return record
            except Exception as exc:
                await db.rollback()
                log_exception(request, f"DB commit failed: {str(exc)}")
                raise HTTPException(status_code=400, detail=str(exc))

            finally:
                end_span(request)  # db_commit
        else:
            log_warning(request, f"Contract {contract_id} not found")
            return "Contract not Found"

    except Exception as exc:
        log_exception(request, f"Update contract route failed: {str(exc)}")
        raise
    finally:
        end_span(request)

@contract_router.delete("/{contract_id}")
async def delete_contract(request:Request,contract_id: int, db: AsyncSession = Depends(get_async_session)):
    new_span(request, "delete_contract_route")
    try:
        new_span(request, "fetch_contract_db")
        result = await db.execute(select(Contract).where(Contract.id == contract_id))
        record = result.scalars().first()
        end_span(request)  # fetch_contract_db
        if record:
            new_span(request, "db_delete")
            await db.delete(record)
            await db.commit()
            end_span(request)  # db_delete
            log_info(request, f"Contract {contract_id} deleted successfully")
            return "Deleted successfully"
        else:
            log_warning(request, f"Contract {contract_id} not found")
            return "No Record Found"

    except Exception as exc:
        await db.rollback()
        log_exception(request, f"Delete contract route failed: {str(exc)}")
        raise
    finally:
        end_span(request)

