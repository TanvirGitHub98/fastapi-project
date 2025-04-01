from pydantic import BaseModel

#pydantic model used for request & response, does not interact with db

class Basepost(BaseModel):
    title:str
    content:str
    published:bool=True
    
    
class Postcreate(Basepost):
    pass


class Postresponse(Basepost):
    id:int
    class Config:  # For Pydantic v1
        orm_mode = True
