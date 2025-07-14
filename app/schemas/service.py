from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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