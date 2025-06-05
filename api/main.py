from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import agents, chat  # یا تنظیمات، اگر اضافه کردی
from api.endpoints import environments
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در محیط واقعی محدود کن
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(environments.router, prefix="/environments", tags=["Environments"])
