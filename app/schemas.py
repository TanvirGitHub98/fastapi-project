from pydantic import BaseModel

#pydantic model used for request & response, does not interact with db

class Basepost(BaseModel):
    title:str
    content:str
    published:bool=True
    
    
class Postcreate(Basepost):
    pass