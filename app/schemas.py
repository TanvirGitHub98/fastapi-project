from pydantic import BaseModel,EmailStr
from typing import Optional

#pydantic model used for request & response, does not interact with db

class Basepost(BaseModel):
    title:str
    content:str
    published:bool=True
    
    
class Postcreate(Basepost):
    pass


class Postresponse(Basepost):
    id:int
    owner_id:int
    class Config:  # For Pydantic v1
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password:str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    
    class Config:
        orm_mode=True    



class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional['str']=None        