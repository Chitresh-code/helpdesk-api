from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.service_request import ServiceStatus

class ServiceRequestResponse(BaseModel):
    id: Optional[int]
    service_id: int
    requester_name: str
    request_date: datetime
    status: ServiceStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class CreateServiceRequestResponse(BaseModel):
    status: str
    message: str
    data: ServiceRequestResponse

class ListServiceRequestsResponse(BaseModel):
    status: str
    message: str
    data: List[ServiceRequestResponse]

class UpdateServiceRequestStatusResponse(BaseModel):
    status: str
    message: str
    data: Optional[ServiceRequestResponse]