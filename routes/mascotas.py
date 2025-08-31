from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.mascota import MascotaCreate, MascotaUpdate
from database.db import dueños_collection, mascotas_collection, serialize_doc

router = APIRouter()

# Endpoints Mascotas
@router.get("/mascotas", tags=["Mascotas"])
def read_mascotas():
    mascotas = list(mascotas_collection.find())
    return JSONResponse(content={"mascotas": [serialize_doc(m) for m in mascotas]})

@router.get("/mascotas/{mascota_id}", tags=["Mascotas"])
def read_mascota(mascota_id: str):
    mascota = mascotas_collection.find_one({"_id": ObjectId(mascota_id)})
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return JSONResponse(content={"mascota": serialize_doc(mascota)})

@router.post("/mascotas", tags=["Mascotas"])
def create_mascota(mascota: MascotaCreate):
    if not dueños_collection.find_one({"_id": ObjectId(mascota.id_dueño)}):
        raise HTTPException(status_code=400, detail="Dueño no existe")
    mascota_dict = mascota.dict()
    mascota_dict["id_dueño"] = ObjectId(mascota.id_dueño)
    result = mascotas_collection.insert_one(mascota_dict)
    return JSONResponse(content={"message": "Mascota creada exitosamente", "id": str(result.inserted_id)}, status_code=201)

@router.put("/mascotas/{mascota_id}", tags=["Mascotas"])
def update_mascota(mascota_id: str, mascota: MascotaUpdate):
    existing = mascotas_collection.find_one({"_id": ObjectId(mascota_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    update_data = mascota.dict(exclude_unset=True)
    if "id_dueño" in update_data:
        if not dueños_collection.find_one({"_id": ObjectId(update_data["id_dueño"])}):
            raise HTTPException(status_code=400, detail="Nuevo dueño no existe")
        update_data["id_dueño"] = ObjectId(update_data["id_dueño"])
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    mascotas_collection.update_one(
        {"_id": ObjectId(mascota_id)},
        {"$set": update_data}
    )
    return JSONResponse(content={
        "message": "Mascota actualizada exitosamente",
        "mascota": serialize_doc(mascotas_collection.find_one({"_id": ObjectId(mascota_id)}))
    })

@router.delete("/mascotas/{mascota_id}", tags=["Mascotas"])
def delete_mascota(mascota_id: str):
    result = mascotas_collection.delete_one({"_id": ObjectId(mascota_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return JSONResponse(content={"message": "Mascota eliminada exitosamente"})
