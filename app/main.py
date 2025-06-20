# app/main.py

from fastapi import FastAPI
from app.api.v1.routes import data_importer, users, sessions, messages,data_importer,data_manager
from app.core.config import settings
from app.database.session import engine
from fastapi.middleware.cors import CORSMiddleware



# Import models so Base has them before creating tables
from app.models.user import User
from app.models.session import Session
from app.models.message import Message

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])
app.include_router(data_importer.router,prefix="/api/v1", tags=["import"])
app.include_router(data_manager.router,prefix="/api/v1", tags=["manage data"])
@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}


# -----------------------------
# Create DB tables on startup
# -----------------------------
@app.on_event("startup")
def initialize_database():
    from sqlalchemy.ext.declarative import declarative_base
    from app.database.session import Base
    Base.metadata.create_all(bind=engine)
