from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.service import Service

async def get_services(session: AsyncSession):
    """Fetch all services from the database."""
    try:
        result = await session.exec(select(Service))
        services = result.all()
        return services
    except Exception as e:
        print(f"Error fetching services: {e}")
        return []
    
async def create_service(session: AsyncSession, service_data: dict):
    """Create a new service in the database."""
    try:
        service = Service(**service_data)
        session.add(service)
        await session.commit()
        await session.refresh(service)
        return service
    except Exception as e:
        print(f"Error creating service: {e}")
        return None

async def update_service_quantity(session: AsyncSession, service_id: int, quantity: int):
    """Update the quantity of a service."""
    try:
        service = await session.get(Service, service_id)
        if service:
            service.quantity = quantity
            session.add(service)
            await session.commit()
            await session.refresh(service)
            return service
        else:
            print(f"Service with id {service_id} not found.")
            return None
    except Exception as e:
        print(f"Error updating service quantity: {e}")
        return None