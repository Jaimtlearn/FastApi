from typing import List, Optional
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)

import models
from database import get_db
from schemas import Post, PostResponse, CreatePost
from oauth import get_current_user


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Geting all posts
@router.get('/', response_model=List[PostResponse])
async def post(db: Session = Depends(get_db), curr_user: int = Depends(get_current_user),
     limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if limit == 0:
        if search != "":
            result = db.query(models.Post).filter(models.Post.title.contains(search)).all()
            return result
        result = db.query(models.Post).all()
        return result
    else:
        if search != "":
            result = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
            return result
        result = db.query(models.Post).limit(limit).offset(offset).all()
        return result
        

# Getting latest post
@router.get('/latest')
async def get_post(db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    result = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"latest post" : result}

# getting specific post through id
@router.get('/{id}')
async def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    result = db.query(models.Post).where(models.Post.id==id).first()
    if result:
        return {"data" : result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post id not found")

# creating post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    user_data = post.model_dump()
    # result = models.Post(title=user_data["title"],content=user_data["content"], published=user_data["published"])
    result = models.Post(owner_id=curr_user.id, **user_data)
    db.add(result)
    db.commit()
    db.refresh(result) # similar to returning statement
    return result
    # raise HTTPException(status_code=status.HTTP_201_CREATED, detail="post created successfully")

# Deleting post through id
@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == id)
    user = result.first()
    if user:
        if curr_user.id != user.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for requested action")
        result.delete(synchronize_session=False)
        db.commit()
        return {"msg" : "Delete successfull"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post id not found")

# For Updating post through id
@router.put('/{id}', response_model=PostResponse )
async def update_post(id : int, post: Post, db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == id)
    query_result = result.first()
    if query_result != None:
        if curr_user.id != query_result.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for requested action")
        user_data = post.model_dump()
        result.update(user_data,synchronize_session=False)
        db.commit()
        return {"Updated Successfully" : result.first()}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")