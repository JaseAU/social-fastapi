from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, query
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.voter_id == current_user.user_id)
    found_vote = vote_query.first()
    #Upvote
    if (vote.updown == 1):
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.user_id} has already voted on post {vote.post_id}.")
        new_vote = models.Vote(post_id=vote.post_id, voter_id=current_user.user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    
    #Downvote
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.user_id} has not yet voted on post {vote.post_id}.")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
    
    #vote = db.query(models.Vote).filter(models.PostLike.id == id)
    #postlike.update()
    #db.commit()