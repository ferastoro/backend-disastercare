from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
import app.models

from app.routes import (
    auth,
    disasters,
    registrations,
    tasks,
    supplies,
    reports,
    shelters,
    shelter_needs,
    users,
    activity_logs,
    dashboard,
    uploads,
)

app = FastAPI(title="DisasterCare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pastikan folder upload ada
os.makedirs("uploads", exist_ok=True)

# Membuat tabel yang belum ada
Base.metadata.create_all(bind=engine)

# Static file untuk akses attachment/foto yang diupload
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Router lama
app.include_router(auth.router)
app.include_router(disasters.router)
app.include_router(registrations.router)
app.include_router(tasks.router)
app.include_router(supplies.router)
app.include_router(reports.router)

# Router tambahan untuk melengkapi frontend final
app.include_router(shelters.router)
app.include_router(shelter_needs.router)
app.include_router(users.router)
app.include_router(activity_logs.router)
app.include_router(dashboard.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {"message": "DisasterCare API is running"}