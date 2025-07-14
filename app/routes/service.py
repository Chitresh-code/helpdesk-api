from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from app.db.init_db import AsyncSessionLocal
from app.crud.service import get_services, update_service_quantity, create_service
from app.schemas.service import (
    CreateServiceResponse,
    ListServicesResponse,
    UpdateServiceQuantityResponse,
)

service_router = APIRouter()

# Dependency to get DB session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Get all services
@service_router.get("/", response_model=ListServicesResponse)
async def read_services(session: AsyncSession = Depends(get_session)):
    try:
        services = await get_services(session)
        return {
            "status": "success",
            "message": "Services retrieved successfully",
            "data": services
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create new service
@service_router.post("/", response_model=CreateServiceResponse)
async def create_new_service(service: dict, session: AsyncSession = Depends(get_session)):
    try:
        new_service = await create_service(session, service)
        return {
            "status": "success",
            "message": "Service created successfully",
            "data": new_service
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update quantity
@service_router.put("/{service_id}/quantity", response_model=UpdateServiceQuantityResponse)
async def modify_service_quantity(service_id: int, quantity: int, session: AsyncSession = Depends(get_session)):
    try:
        updated_service = await update_service_quantity(session, service_id, quantity)
        if not updated_service:
            raise HTTPException(status_code=404, detail="Service not found")
        return {
            "status": "success",
            "message": "Service quantity updated successfully",
            "data": updated_service
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))