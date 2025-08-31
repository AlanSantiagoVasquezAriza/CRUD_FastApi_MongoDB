from fastapi import FastAPI
from routes.dueños import router as dueños_router
from routes.mascotas import router as mascotas_router
from routes.root import router as root_router

app = FastAPI(
    title="Mascotas FastAPI",
    description="API para gestionar mascotas y dueños con MongoDB",
    version="1.0.0",
)

app.include_router(root_router)
app.include_router(dueños_router)
app.include_router(mascotas_router)