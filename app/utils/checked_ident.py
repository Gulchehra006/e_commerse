from fastapi import HTTPException


async def check_id(db,model,obj_id):
    obj = await db.get(model,obj_id)
    if not obj:
        raise HTTPException(404,f"{model.__name__} not found")
    return obj