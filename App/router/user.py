from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

sys.path.insert(0, parent_dir)


import models
from database import get_db
from utils import Hash
from schemas import UserCreate, UserResponse

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/', response_model= List[UserResponse])
async def get_user(db: Session = Depends(get_db)):
    query = db.query(models.User).all()
    if query:
        return query
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")

@router.post('/',status_code=status.HTTP_201_CREATED, response_model= UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hased_pwd = Hash(user.password)
        user.password = hased_pwd
        new_user = models.User(email=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        return new_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    
@router.get('/{id}', response_model=UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    query_result = query.first()
    if query_result:
        return query_result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")