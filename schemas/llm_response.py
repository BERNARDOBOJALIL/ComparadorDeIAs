from pydantic import BaseModel, Field
from typing import Optional


class LLMResponse(BaseModel):
    """Schema simple para validar respuestas JSON de LLMs"""
    
    respuesta: str = Field(..., description="Respuesta del modelo")
    confianza: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nivel de confianza (0-1)")
    categoria: Optional[str] = Field(None, description="Categoría de la respuesta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "respuesta": "Esta es una respuesta de ejemplo",
                "confianza": 0.95,
                "categoria": "general"
            }
        }
