from jose import JWTError,jwt
from datetime import datetime,timedelta

import pytz
from . import schemas
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
#Secret_key
#Algorithm
#Expiration_time
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY="helloIamjj"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES=1


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(pytz.utc) +timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(id=str())
    except JWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credential",
                                       headers={'WWWW-Authenticate':'Bearer'})
   
    return verify_access_token(token,credential_exception) 