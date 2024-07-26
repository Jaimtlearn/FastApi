from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

sys.path.insert(0, parent_dir)

from schemas import VoteSchema
from models import Vote
from database import get_db
from oauth import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteSchema, db: Session = Depends(get_db), curr_user: dict = Depends(get_current_user)):
    result = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == vote.user_id)
    query = result.first()
    if vote.direction == 1:
        if query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted this post")
        new_vote = Vote(post_id=vote.post_id, user_id=vote.user_id)
        db.add(new_vote)
        db.commit()
        return {"msg" : "Successful added vote"}
    else:
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exists")
        result.delete(synchronize_session=False)
        db.commit()
        return {"msg" : "Successful deleted vote"}

