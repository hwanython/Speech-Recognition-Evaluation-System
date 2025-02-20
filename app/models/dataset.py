from pydantic import BaseModel
from typing import Optional

class DatasetCreate(BaseModel):
    name: str
    collection: str

class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    collection: Optional[str] = None

class DatasetResponse(BaseModel):
    id: str
    name: str
    collection: str 