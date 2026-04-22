import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Security, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.auth.current_user import get_current_user
from app.auth.models import CurrentUser

from app.database.session_factory import get_db
from app.database.models import User, Song

from app.schemas.user import UserRead, UserUpdate, UserCreate
from app.schemas.song import SongUpdate

users_router = APIRouter()
logger = logging.getLogger("app_logger") # Configure inside app/__main__.py

@users_router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: CurrentUser = Security(get_current_user)):

    logger.info(f"[User: {current_user.username or current_user.sub}] -  Received Request at GET: /users/{user_id}")

    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result

def update_user_songs(user: User, updated_user_songs: list[SongUpdate]) -> User:
    """
    Takes in a user and the payload list of updated songs
    Returns a new array of reconciled songs
    """

    reconciled_songs = []

    # Create a dict of the existing songs
    current_user_songs = {song.id: song for song in user.songs} 

    for incoming in updated_user_songs:
        if incoming.get("id", None):
            song = current_user_songs.get(incoming.get("id"))
            if not song:
                raise ValueError("Invalid song id")
            reconciled_songs.append(song)
        else:
            reconciled_songs.append(
                Song(**song)
            )
    
    user.songs = reconciled_songs
    return user
        


@users_router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Security(get_current_user)):

    complex_attributes = ["songs"]
    
    logger.info(f"[User: {current_user.username or current_user.sub}] -  Received Request at PUT: /users/{user_id}")

    # Model dump the payload
    # exclude_unset=True means don't assume unprovided values are None and only update provided valus
    user_data = user_data.model_dump(exclude_unset=True)

    stmt = select(User).where(User.id == user_id)
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # loop over payload attributes and update ORM obj atrributes
    for key, value in user_data.items():
        if key in complex_attributes and key == "songs":
            user = update_user_songs(user, value)
        else:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@users_router.post("/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: CurrentUser = Security(get_current_user)):

    logger.info(f"[User: {current_user.username or current_user.sub}] -  Received Request at POST: /users")

    # Model dump the payload
    payload = user_data.model_dump()

    # Handle created_at
    now = datetime.now(timezone.utc)
    payload['created_at'] = now

    user = User(**payload)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
