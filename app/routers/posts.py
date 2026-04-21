from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import models, schemas, Oauth2
from database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)


# get all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    # print(posts)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    #return {"data": posts}
    return posts # FastAPI will automatically convert the SQLAlchemy models to JSON serializable format

# create new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_new_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user)
    new_post = models.Post(**post.model_dump()) # Unpacking the post object into the Post model.. effectively the same as the line above..
    db.add(new_post)
    db.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post could not be created")
    db.refresh(new_post) # Refresh the instance to get the generated ID and other fields
    #return {"data": new_post}
    return new_post

# get post by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    #return {"data": post}
    return post

# delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post by id
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post_by_id(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    post_query.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    #return {"data": post_query.first()}
    return post_query.first()
