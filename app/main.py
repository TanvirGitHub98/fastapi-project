from random import randrange
from fastapi import  FastAPI, HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel, Field
app=FastAPI()

class User(BaseModel):
    name:str
    age:int =Field(strict=True)
 


myUser=[{"id":1,"name":"Rony","age":30},{"id":2,"name":"Mimi","age":20}]   

def checkId(id):
        
 for p in myUser:
     if p['id']== id:
         return p
         


def findUserForById(id):
    for i,p in enumerate(myUser):
        if p['id']==id:
            return i
          
    

@app.get('/')
async def root():
    return{"All User":myUser}

@app.post('/createAccount',status_code=status.HTTP_201_CREATED)
async def createAccount(newUser:User):
    userDict=newUser.model_dump()
    userDict['id']=randrange(0,1000000)
    myUser.append(userDict)
    
    
    return{
        "new User": myUser
    }
    
@app.get('/getById/{id}')
async def getById(id:int):
    Id=checkId(id)
    if not Id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id :{id} not found")
        return
    return{
        "Id":Id
    }
    
    
@app.delete('/deleteUserById/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def deleteUserById(id:int):
    
    res=findUserForById(id)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User Id: {id} Not Found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@app.put('/updateUserById/{id}')
async def updateUser(id:int,user:User):
    index=findUserForById(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id {id} is not available")

    userData=user.model_dump()
    userData['id']=id
    myUser[index]=userData
    return {"message": "User updated successfully", "updatedUser": userData}

