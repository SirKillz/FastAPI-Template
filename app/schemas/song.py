from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SongRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    artist: str | None

class SongUpdate(BaseModel):
    id: int | None = None
    name: str
    artist: str