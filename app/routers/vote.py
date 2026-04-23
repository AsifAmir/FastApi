from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import models, schemas, Oauth2
from database import get_db

router = APIRouter(
    prefix = "/vote",
    tags=["Vote"]
)

# create new vote
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the user has already voted on this post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:  # User wants to upvote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else:  # User wants to remove their vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
