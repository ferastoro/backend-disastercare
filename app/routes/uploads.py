import os
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    extension = file.filename.split(".")[-1]
    safe_filename = f"{uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": safe_filename,
        "path": file_path,
        "url": f"/uploads/{safe_filename}"
    }