import logging
from typing import Annotated

from fastapi import APIRouter, Security, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app_name.Auth.current_user import get_current_user
from app_name.Auth.models import CurrentUser

from app_name.database.database import get_db

test_db_router = APIRouter()
logger = logging.getLogger("app_logger") # Configure inside src/app/__main__.py

@test_db_router.get("/test/db/{some_id}")
async def test(some_id: int, db: Annotated[Session, Depends(get_db)], current_user: CurrentUser = Security(get_current_user)):

    logger.info(f"[User: {current_user.username or current_user.sub}] -  Received Request at /test")

    # result = db.execute(
    #     select(some_model).where(some_model.id == some_id)
    # )
    # item = result.scalars().first()

    # return item