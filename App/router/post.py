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
from schemas import Post, PostResponse, CreatePost
from oauth import get_current_user


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Geting all posts

@router.get('/', response_model=List[PostResponse])
async def post(db: Session = Depends(get_db)):
    # cursor.execute(""" 
                   
    #                SELECT * FROM posts; 
                   
    #                """)
    # result = cursor.fetchall()
    result = db.query(models.Post).all()
    return result

# Getting latest post
@router.get('/latest')
async def get_post(db: Session = Depends(get_db)):
    # cursor.execute("""
                   
    #     SELECT * FROM posts
    #     ORDER BY created_at DESC LIMIT 1;
                   
    #                """)
    # result = cursor.fetchall()
    result = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"latest post" : result}

# getting specific post through id
@router.get('/{id}')
async def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
                   
    #         SELECT * FROM posts
    #         WHERE id = %s
                    
    #                 """,str(id))
    # result = cursor.fetchall()
    result = db.query(models.Post).where(models.Post.id==id).first()
    if result:
        return {"data" : result}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post id not found")

# creating post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(get_current_user)):
    # data = post.model_dump()
    # cursor.execute("""
                   
    #         INSERT INTO posts (title,content,published)
    #         VALUES (%s, %s, %s) RETURNING *;
                   
    #             """,(data['title'], data['content'], data['published']))
    # result = cursor.fetchone()
    # conn.commit()
    print(curr_user)
    user_data = post.model_dump()
    # result = models.Post(title=user_data["title"],content=user_data["content"], published=user_data["published"])
    result = models.Post(**user_data)
    db.add(result)
    db.commit()
    db.refresh(result) # similar to returning statement
    return result
    # raise HTTPException(status_code=status.HTTP_201_CREATED, detail="post created successfully")

# Deleting post through id
@router.delete('/{id}')
async def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
                   
    #             DELETE FROM posts
    #             WHERE id = %s RETURNING *;

    #                 """, str(id))
    # result = cursor.fetchone()
    # conn.commit()
    result = db.query(models.Post).filter(models.Post.id == id)
    user = result.first()
    if user:
        result.delete(synchronize_session=False)
        db.commit()
        return {"msg" : "Delete successfull"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post id not found")

# For Updating post through id
@router.put('/{id}')
async def update_post(id : int, post: Post, db: Session = Depends(get_db)):
    # post = post.model_dump()
    # cursor.execute("""

    #         UPDATE posts
    #         SET title=%s, content=%s, published=%s
    #         WHERE id = %s RETURNING *;
                   
    #         """,(post["title"],post["content"],post["published"],str(id)))
    # result = cursor.fetchone()
    # conn.commit()
    user_data = post.model_dump()
    result = db.query(models.Post).filter(models.Post.id == id)
    query_result = result.first()
    if query_result != None:
        result.update(user_data,synchronize_session=False)
        db.commit()
        return {"Updated Successfully" : result.first()}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")