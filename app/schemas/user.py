from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict

from app.schemas.song import SongUpdate

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool | None
    created_at: datetime | None

class UserUpdate(BaseModel):
    
    email: str | None = None
    is_active: bool | None = None
    songs: list[SongUpdate] | None = None

class UserCreate(BaseModel):

    email: str
    is_active: bool | None = False
    user_metadata: Dict | None = None
    # created_at will be handled on backend