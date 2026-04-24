from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils

router = APIRouter(
    prefix = "/users",
    tags=["Users"]
)

# create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password) # Hash the password before storing it in the database
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created")
    db.refresh(new_user)
    return new_user

# get user by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserCreateResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user