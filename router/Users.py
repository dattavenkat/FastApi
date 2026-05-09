from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from typing import Annotated
from passlib.context import CryptContext
from models import Todos, Users
from database import SessionLocal
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix='/Users',
    tags=['Users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PassRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/",  status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()



@router.put("/todo/", status_code= status.HTTP_204_NO_CONTENT)
async def put_item(user: user_dependency, db: db_dependency, passer: PassRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="item not found")

    if not bcrypt_context.verify(passer.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(passer.new_password)
    db.add(user_model)
    db.commit()




@router.put("/phone_number/", status_code= status.HTTP_204_NO_CONTENT)
async def put_item(user: user_dependency, db: db_dependency, passer: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not user_model:
        raise HTTPException(status_code=404, detail="item not found")

    user_model.phone_number = passer
    db.add(user_model)
    db.commit()
















