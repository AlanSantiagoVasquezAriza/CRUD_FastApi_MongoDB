from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from models.mascota import MascotaCreate, MascotaUpdate
from database.db import dueños_collection, mascotas_collection, serialize_doc
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

router = APIRouter()

@router.get("/mascotas/{mascota_id}/raza", tags=["IA"])
def get_raza(mascota_id: str):
    try:
        # Buscar mascota en la colección
        mascota = mascotas_collection.find_one({"_id": ObjectId(mascota_id)})
        if not mascota:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")

        # Extraer la raza (campo tipo)
        raza = mascota.get("tipo")
        if not raza:
            raise HTTPException(status_code=400, detail="La mascota no tiene definida una raza")

        # Preguntar a la IA sobre la raza
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  # Opcional
                "X-Title": "<YOUR_SITE_NAME>",      # Opcional
            },
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un veterinario experto en animales domésticos. Tu misión es dar información clara, confiable y entretenida sobre las razas de perros."
                },
                {
                    "role": "user",
                    "content": f"Dame 3 datos interesantes, curiosos o poco conocidos sobre la raza {raza}. Incluye información sobre su personalidad, historia o cuidados especiales, y exprésalo en un lenguaje sencillo y amigable."
                }
            ]

        )

        # Respuesta de la IA + datos de la mascota
        return JSONResponse(content={
            "mascota": serialize_doc(mascota),
            "raza": raza,
            "datos_interesantes": completion.choices[0].message.content
        })

    except Exception as e:
        return {"error": str(e)}