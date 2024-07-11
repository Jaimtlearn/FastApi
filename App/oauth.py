from jose import JWTError, jwt
import copy
from datetime import datetime, timedelta, timezone
from schemas import Token, TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
from models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl='auths/login')

SECRET_KEY = 'd74b2c89c4ba7de9fc6b49740148947f4b11b14d3620682b7619593584203eff'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    data = copy.deepcopy(payload)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp" : expire})
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id:
            token_data = TokenData(id=id)
            return token_data
        raise credentials_exception
    except JWTError:
        raise credentials_exception

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
    
