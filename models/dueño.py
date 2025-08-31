from pydantic import BaseModel, Field, constr, validator
from typing import Optional
import re

class DueñoCreate(BaseModel):
    nombre: str = Field(..., min_length=5)
    direccion: str = Field(..., min_length=5)
    telefono: constr(min_length=5, max_length=10) = Field(...) # type: ignore

    @validator('telefono')
    def telefono_numerico(cls, v):
        if not re.fullmatch(r'^[0-9]+$', v):
            raise ValueError('El teléfono debe contener solo números')
        return v

class DueñoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=5)
    direccion: Optional[str] = Field(None, min_length=5)
    telefono: Optional[constr(min_length=5, max_length=10)] = None # type: ignore