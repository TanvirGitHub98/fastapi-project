from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import engine,get_db
from fastapi import  Depends, FastAPI, HTTPException, Response,status,APIRouter


router=APIRouter(
    
    tags=['Users']
)


@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    #hash the password
    user.password=utils.hash(user.password)
    
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    

@router.get("/users/{id}",status_code=status.HTTP_200_OK)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User Not Found with id:{id}")
    return user    