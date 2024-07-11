from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

from database import get_db
from schemas import Userlogin, Token
from utils import Verify
from oauth import create_access_token
import models

router = APIRouter(
    prefix='/auths',
    tags=['Authentication']
    )

@router.post('/login', response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query_result = db.query(models.User).filter(models.User.email == user.username).first()
    if query_result:
        if Verify(user.password, query_result.password):
            token = create_access_token(payload={"user_id" : query_result.id})
            return {"access_token" : token, "token_type" : "bearer"}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")