from jose import JWTError,jwt
from datetime import datetime,timedelta

#Secret_key
#Algorithm
#Expiration_time

SECRET_KEY="helloIamjj"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES=30


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now() +timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    
