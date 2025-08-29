from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker, query
from app import models, schemas, utils
from app.database import get_db

router = APIRouter(
    prefix = "/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.passowrd
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found.")        
    return user