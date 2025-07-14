from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi.responses import JSONResponse

from app.db.init_db import AsyncSessionLocal
from app.crud.service import (
    get_services,
    update_service_quantity,
    create_service,
)
from app.schemas.service import (
    ServiceCreateSchema,
    UpdateServiceQuantitySchema,
    CreateServiceResponse,
    ListServicesResponse,
    UpdateServiceQuantityResponse,
)

service_router = APIRouter()

# Dependency to get DB session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# ------------------ GET: All Services ------------------
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
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# ------------------ POST: Create New Service ------------------
@service_router.post("/", response_model=CreateServiceResponse)
async def create_new_service(
    service: ServiceCreateSchema,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_service = await create_service(session, service.dict())
        if not new_service:
            return JSONResponse({"status": "error", "message": "Failed to create service"}, status_code=500)
        return {
            "status": "success",
            "message": "Service created successfully",
            "data": new_service
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# ------------------ PUT: Update Service Quantity ------------------
@service_router.put("/{service_id}/quantity", response_model=UpdateServiceQuantityResponse)
async def modify_service_quantity(
    service_id: int,
    payload: UpdateServiceQuantitySchema,
    session: AsyncSession = Depends(get_session)
):
    try:
        updated_service = await update_service_quantity(session, service_id, payload.quantity)
        if not updated_service:
            return JSONResponse({"status": "error", "message": "Service not found"}, status_code=404)
        return {
            "status": "success",
            "message": "Service quantity updated successfully",
            "data": updated_service
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)