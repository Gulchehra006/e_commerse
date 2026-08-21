from fastapi import APIRouter, UploadFile, File
from app.utils.save_file import save_image


router = APIRouter(tags=["Upload File"])


@router.post("/save_file")
async def save_file(file: UploadFile = File(...)):
    filename = await save_image(file)
    return {"message": "Upload Success !", "filename": filename}
