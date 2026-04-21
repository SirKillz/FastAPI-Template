from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool | None
    created_at: datetime | None

class UserUpdate(BaseModel):
    
    email: str | None
    is_active: bool | None

class UserCreate(BaseModel):

    email: str
    is_active: bool | None
    # created_at will be handled on backend