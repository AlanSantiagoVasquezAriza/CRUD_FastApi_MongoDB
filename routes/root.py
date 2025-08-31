from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
    
from database.db import dueños_collection, serialize_doc

router = APIRouter()

# Root
@router.get("/", tags=["root"])
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