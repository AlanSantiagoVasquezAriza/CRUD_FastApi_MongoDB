from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.dueño import DueñoCreate, DueñoUpdate
from database.db import dueños_collection, serialize_doc

router = APIRouter()

# Endpoints Dueños
@router.get("/dueños", tags=["Dueños"])
def read_dueños():
    dueños = list(dueños_collection.find())
    return JSONResponse(content={"dueños": [serialize_doc(d) for d in dueños]})

@router.get("/dueños/{dueño_id}", tags=["Dueños"])
def read_dueño(dueño_id: str):
    dueño = dueños_collection.find_one({"_id": ObjectId(dueño_id)})
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return JSONResponse(content={"dueño": serialize_doc(dueño)})

@router.post("/dueños", tags=["Dueños"])
def create_dueño(dueño: DueñoCreate):
    result = dueños_collection.insert_one(dueño.dict(by_alias=True, exclude={"id"}))
    return JSONResponse(content={"message": "Dueño creado exitosamente", "id": str(result.inserted_id)}, status_code=201)

@router.put("/dueños/{dueño_id}", tags=["Dueños"])
def update_dueño(dueño_id: str, dueño: DueñoUpdate):
    existing = dueños_collection.find_one({"_id": ObjectId(dueño_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    update_data = dueño.dict(exclude={"id"}, exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    dueños_collection.update_one(
        {"_id": ObjectId(dueño_id)},
        {"$set": update_data}
    )
    return JSONResponse(content={
        "message": "Dueño actualizado exitosamente",
        "dueño": serialize_doc(dueños_collection.find_one({"_id": ObjectId(dueño_id)}))
    })

@router.delete("/dueños/{dueño_id}", tags=["Dueños"])
def delete_dueño(dueño_id: str):
    result = dueños_collection.delete_one({"_id": ObjectId(dueño_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return JSONResponse(content={"message": "Dueño eliminado exitosamente"})
