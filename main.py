# env/Script/activate
# uvicorn main:app --reload --port 3000

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# -----------------------------------------------------------------
# Conexión a MongoDB
# -----------------------------------------------------------------
load_dotenv() # Cargar variables desde el archivo .env
client = MongoClient(os.getenv("MONGO_URI"))
db = client["MascotasDB"]

# Colecciones
dueños_collection = db["dueños"]
mascotas_collection = db["mascotas"]

# -----------------------------------------------------------------
# FastAPI app
# -----------------------------------------------------------------
app = FastAPI(
    title="Mascotas FastAPI",
    description="API para gestionar mascotas y dueños con MongoDB",
    version="1.0.0",
)

# -----------------------------------------------------------------
# Modelos
# -----------------------------------------------------------------
class Dueño(BaseModel):
    id: Optional[str] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class Mascota(BaseModel):
    id: Optional[str] = None
    id_dueño: Optional[str] = None
    nombre: Optional[str] = None
    edad: Optional[int] = None
    tipo: Optional[str] = None

# Función para convertir ObjectId a str
def serialize_doc(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc


# -----------------------------------------------------------------
# Root
# -----------------------------------------------------------------
@app.get("/", tags=["root"])
def read_root():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "mascotas",
                    "localField": "_id",
                    "foreignField": "id_dueño",
                    "as": "mascotas"
                }
            }
        ]
        dueños = list(dueños_collection.aggregate(pipeline))
        for d in dueños:
            d["id"] = str(d["_id"])
            d["mascotas"] = [serialize_doc(m) for m in d["mascotas"]]
            del d["_id"]
        return JSONResponse(content={"Usuarios": dueños})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------
# Endpoints Dueños
# -----------------------------------------------------------------
@app.get("/dueños", tags=["Dueños"])
def read_dueños():
    dueños = list(dueños_collection.find())
    return JSONResponse(content={"dueños": [serialize_doc(d) for d in dueños]})

@app.get("/dueños/{dueño_id}", tags=["Dueños"])
def read_dueño(dueño_id: str):
    dueño = dueños_collection.find_one({"_id": ObjectId(dueño_id)})
    if not dueño:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return JSONResponse(content={"dueño": serialize_doc(dueño)})

@app.post("/dueños", tags=["Dueños"])
def create_dueño(dueño: Dueño):
    result = dueños_collection.insert_one(dueño.dict(exclude={"id"}))
    return JSONResponse(content={"message": "Dueño creado exitosamente", "id": str(result.inserted_id)}, status_code=201)

@app.put("/dueños/{dueño_id}", tags=["Dueños"])
def update_dueño(dueño_id: str, dueño: Dueño):
    # buscar dueño existente
    existing = dueños_collection.find_one({"_id": ObjectId(dueño_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    # solo tomar los campos enviados
    update_data = dueño.dict(exclude={"id"}, exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    result = dueños_collection.update_one(
        {"_id": ObjectId(dueño_id)},
        {"$set": update_data}
    )
    return JSONResponse(content={
        "message": "Dueño actualizado exitosamente",
        "dueño": serialize_doc(dueños_collection.find_one({"_id": ObjectId(dueño_id)}))
    })


@app.delete("/dueños/{dueño_id}", tags=["Dueños"])
def delete_dueño(dueño_id: str):
    result = dueños_collection.delete_one({"_id": ObjectId(dueño_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return JSONResponse(content={"message": "Dueño eliminado exitosamente"})

# -----------------------------------------------------------------
# Endpoints Mascotas
# -----------------------------------------------------------------
@app.get("/mascotas", tags=["Mascotas"])
def read_mascotas():
    mascotas = list(mascotas_collection.find())
    return JSONResponse(content={"mascotas": [serialize_doc(m) for m in mascotas]})

@app.get("/mascotas/{mascota_id}", tags=["Mascotas"])
def read_mascota(mascota_id: str):
    mascota = mascotas_collection.find_one({"_id": ObjectId(mascota_id)})
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return JSONResponse(content={"mascota": serialize_doc(mascota)})

@app.post("/mascotas", tags=["Mascotas"])
def create_mascota(mascota: Mascota):
    # validar que el dueño exista
    if not dueños_collection.find_one({"_id": ObjectId(mascota.id_dueño)}):
        raise HTTPException(status_code=400, detail="Dueño no existe")
    mascota_dict = mascota.dict(exclude={"id"})
    mascota_dict["id_dueño"] = ObjectId(mascota.id_dueño)
    result = mascotas_collection.insert_one(mascota_dict)
    return JSONResponse(content={"message": "Mascota creada exitosamente", "id": str(result.inserted_id)}, status_code=201)

@app.put("/mascotas/{mascota_id}", tags=["Mascotas"])
def update_mascota(mascota_id: str, mascota: Mascota):
    existing = mascotas_collection.find_one({"_id": ObjectId(mascota_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    update_data = mascota.dict(exclude={"id"}, exclude_unset=True)
    # si mandan un nuevo dueño, validarlo
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

@app.delete("/mascotas/{mascota_id}", tags=["Mascotas"])
def delete_mascota(mascota_id: str):
    result = mascotas_collection.delete_one({"_id": ObjectId(mascota_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return JSONResponse(content={"message": "Mascota eliminada exitosamente"})
