from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

class ServiceStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    returned = "returned"

class ServiceRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="service.id", index=True)
    requester_name: str = Field(max_length=100)
    request_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    status: ServiceStatus = Field(default=ServiceStatus.pending, nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"<ServiceRequest(id={self.id}, service_id={self.service_id}, requester_name={self.requester_name})>"