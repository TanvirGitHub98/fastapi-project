from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2


router=APIRouter(tags=["Authentication"])


# @router.post('/login')
# def login(user_credential:schemas.UserLogin,db:Session=Depends(database.get_db)):
#     user=db.query(models.User).filter(models.User.email==user_credential.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found")
    
#     if not utils.verifyLogin(user_credential.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Email or password is invallid!!")
#     #create token
#     #return token
#     access_token=oauth2.create_access_token(data={"user_id":user.id})
   
   
    
#     return {"Token": access_token,"token_type":"bearer"}


#using oauthrequest form 

@router.post('/login')
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User not found")
    
    if not utils.verifyLogin(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Email or password is invallid!!")
    #create token
    #return token
    access_token=oauth2.create_access_token(data={"user_id":user.id})
   
   
    
    return {"Token": access_token,"token_type":"bearer"}
    
    
    
