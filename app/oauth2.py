from jose import JWTError,jwt
from datetime import datetime,timedelta

import pytz
from . import schemas,database,models
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
#Secret_key
#Algorithm
#Expiration_time
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')



SECRET_KEY="helloIamjj"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES=30


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(pytz.utc) +timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        print("Checkkkking----",payload)
        id:str=payload.get("user_id")
        
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(id=str())
    except JWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print("Token",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:  # Check if user_id is None or empty
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in token")

        user = db.query(models.User).filter(models.User.id == int(user_id)).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except JWTError as e:
        print(f"DEBUG: JWT Decode Error - {e}")  # Log error for debugging
        raise credentials_exception