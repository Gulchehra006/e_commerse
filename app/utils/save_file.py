from fastapi import HTTPException
import os
import uuid
import shutil

UPLOAD_DIR = "images"

os.makedirs(UPLOAD_DIR,exist_ok=True)

async def save_image(image):
    if image.size > 5*1024*1024:
        raise HTTPException(400,"Rasm hajmi 5 mb dan oshmasin ")

    if not image.filename.endswith(('jpg', 'jpeg', 'png', 'svg', 'jfif')):
        raise HTTPException(400, 'Yuklagan fayl formati mos emas')

    ext = image.filename.split(".")[-1]
    image_name = f"{uuid.uuid4()}.{ext}"

    with open(f"{UPLOAD_DIR}/{image_name}",'wb') as file:
        shutil.copyfileobj(image.file, file)

    return image_name
