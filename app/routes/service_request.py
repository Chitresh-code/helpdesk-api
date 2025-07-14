from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.models.service_request import ServiceRequest
from app.db.init_db import AsyncSessionLocal
from app.crud.service_request import get_service_requests, update_service_request_status, create_service_request
from app.schemas.service_request import (
    CreateServiceRequestResponse,
    ListServiceRequestsResponse,
    UpdateServiceRequestStatusResponse,
)
from fastapi.responses import JSONResponse

service_request_router = APIRouter()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

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

@service_request_router.put("/{request_id}/status", response_model=UpdateServiceRequestStatusResponse)
async def modify_service_request_status(request_id: int, status: str, session: AsyncSession = Depends(get_session)):
    try:
        updated_request = await update_service_request_status(session, request_id, status)
        if updated_request:
            return {
                "status": "success",
                "message": "Service request status updated successfully.",
                "data": updated_request
            }
        else:
            return JSONResponse({"status": "error", "message": "ServiceRequest not found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@service_request_router.post("/", response_model=CreateServiceRequestResponse)
async def create_new_service_request(request: dict, session: AsyncSession = Depends(get_session)):
    try:
        create_request = ServiceRequest(
            service_id=request.get("service_id"),
            requester_name=request.get("requester_name"),
            request_date=request.get("request_date"),
            status=request.get("status")
        )
        new_request = await create_service_request(session, create_request)
        return {
            "status": "success",
            "message": "Service request created successfully.",
            "data": new_request
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)