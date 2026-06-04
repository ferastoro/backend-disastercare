from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models
from app.routes import auth, disasters, registrations, tasks, supplies, reports

app = FastAPI(title="DisasterCare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(disasters.router)
app.include_router(registrations.router)
app.include_router(tasks.router)
app.include_router(supplies.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "DisasterCare API is running"}