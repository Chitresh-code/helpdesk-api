from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from fastapi.responses import JSONResponse

from app.models.service_request import ServiceRequest
from app.db.init_db import AsyncSessionLocal
from app.crud.service_request import (
    get_service_requests,
    update_service_request_status,
    create_service_request,
)
from app.schemas.service_request import (
    ServiceRequestCreateSchema,
    UpdateServiceRequestStatusSchema,
    CreateServiceRequestResponse,
    ListServiceRequestsResponse,
    UpdateServiceRequestStatusResponse,
)

service_request_router = APIRouter()

# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# ------------------ GET: All Service Requests ------------------
@service_request_router.get("/", response_model=ListServiceRequestsResponse)
async def read_service_requests(session: AsyncSession = Depends(get_session)):
    try:
        service_requests = await get_service_requests(session)
        return {
            "status": "success",
            "message": "Service requests retrieved successfully.",
            "data": service_requests
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# ------------------ POST: Create New Service Request ------------------
@service_request_router.post("/", response_model=CreateServiceRequestResponse)
async def create_new_service_request(
    request: ServiceRequestCreateSchema,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_request = ServiceRequest(**request.dict())
        created = await create_service_request(session, new_request)
        return {
            "status": "success",
            "message": "Service request created successfully.",
            "data": created
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# ------------------ PUT: Update Status ------------------
@service_request_router.put("/{request_id}/status", response_model=UpdateServiceRequestStatusResponse)
async def modify_service_request_status(
    request_id: int,
    payload: UpdateServiceRequestStatusSchema,
    session: AsyncSession = Depends(get_session)
):
    try:
        updated = await update_service_request_status(session, request_id, payload.status)
        if updated:
            return {
                "status": "success",
                "message": "Service request status updated successfully.",
                "data": updated
            }
        else:
            return JSONResponse({"status": "error", "message": "ServiceRequest not found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
