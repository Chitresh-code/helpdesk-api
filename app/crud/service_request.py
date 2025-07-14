from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.service_request import ServiceRequest

async def get_service_requests(session: AsyncSession):
    """Fetch all service requests from the database."""
    try:
        result = await session.exec(select(ServiceRequest))
        service_requests = result.all()
        return service_requests
    except Exception as e:
        print(f"Error fetching service requests: {e}")
        return []
    
async def create_service_request(session: AsyncSession, service_request: ServiceRequest):
    """Create a new service request."""
    try:
        session.add(service_request)
        await session.commit()
        await session.refresh(service_request)
        return service_request
    except Exception as e:
        print(f"Error creating service request: {e}")
        return None
    
async def update_service_request_status(session: AsyncSession, request_id: int, status: str):
    """Update the status of a service request."""
    try:
        service_request = await session.get(ServiceRequest, request_id)
        if service_request:
            service_request.status = status
            session.add(service_request)
            await session.commit()
            await session.refresh(service_request)
            return service_request
        else:
            print(f"ServiceRequest with id {request_id} not found.")
            return None
    except Exception as e:
        print(f"Error updating service request status: {e}")
        return None