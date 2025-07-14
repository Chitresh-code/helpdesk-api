from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.service_request import ServiceStatus

# ------------------ Request Schemas ------------------

class ServiceRequestCreateSchema(BaseModel):
    service_id: int
    requester_name: str = Field(..., max_length=100)
    request_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    status: Optional[ServiceStatus] = Field(default=ServiceStatus.pending)

class UpdateServiceRequestStatusSchema(BaseModel):
    status: ServiceStatus

# ------------------ Shared Output Schema ------------------

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

# ------------------ Response Schemas ------------------

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
