from fastapi import FastAPI
from app.routes.service_request import service_request_router
from app.routes.service import service_router
from app.db.init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # Add cleanup logic here if needed in future

app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(service_request_router, prefix="/api/v1/service-requests", tags=["service_requests"])
app.include_router(service_router, prefix="/api/v1/services", tags=["services"])

# Entry point
def main():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# Only run when script is called directly
if __name__ == "__main__":
    main()