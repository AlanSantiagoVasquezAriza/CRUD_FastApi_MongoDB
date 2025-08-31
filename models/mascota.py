from pydantic import BaseModel, Field, constr
from typing import Optional

class MascotaCreate(BaseModel):
    id_dueño: str = Field(..., description="El id_dueño es obligatorio")
    nombre: str = Field(
        ..., 
        min_length=2, 
        max_length=15, 
        description="El nombre es obligatorio y debe tener entre 2 y 15 caracteres"
    )
    edad: int = Field(
        ..., 
        ge=1, 
        le=99, 
        description="La edad debe estar entre 1 y 99"
    )
    tipo: str = Field(
        ..., 
        description="El tipo es obligatorio"
    )

class MascotaUpdate(BaseModel):
    id_dueño: Optional[str] = Field(None, description="El id_dueño es opcional para actualización")
    nombre: Optional[str] = Field(
        None, 
        min_length=2, 
        max_length=15, 
        description="El nombre debe tener entre 2 y 15 caracteres"
    )
    edad: Optional[int] = Field(
        None, 
        ge=1, 
        le=99, 
        description="La edad debe estar entre 1 y 99"
    )
    tipo: Optional[str] = Field(
        None, 
        description="El tipo es opcional para actualización"
    )