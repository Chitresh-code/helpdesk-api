from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    quantity: int = Field(default=0, ge=0)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name})>"