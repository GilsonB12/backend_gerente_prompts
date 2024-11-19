from pydantic import BaseModel
from typing import Optional

class PromptBase(BaseModel):
    name: str
    content: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    content: Optional[str]  # Apenas o conteúdo pode ser atualizado

class PromptResponse(PromptBase):
    id: int
    version: int
    created_by: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
