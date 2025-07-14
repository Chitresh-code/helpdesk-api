from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ------------------ Request Schema ------------------

class ServiceCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    quantity: int = Field(default=0, ge=0)

class UpdateServiceQuantitySchema(BaseModel):
    quantity: int = Field(..., ge=0, description="New quantity value (must be ≥ 0)")

# ------------------ Shared Output Schema ------------------

class Service(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    quantity: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }

# ------------------ Response Schemas ------------------

class CreateServiceResponse(BaseModel):
    status: str
    message: str
    data: Service

class ListServicesResponse(BaseModel):
    status: str
    message: str
    data: List[Service]

class UpdateServiceQuantityResponse(BaseModel):
    status: str
    message: str
    data: Optional[Service] = None