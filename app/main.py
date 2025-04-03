from random import randrange
from typing import List
from fastapi import  Depends, FastAPI, HTTPException, Response,status
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,utils
from .database import engine,get_db

from .routers import post,user,auth
from fastapi.openapi.utils import get_openapi

#related to db
models.Base.metadata.create_all(bind=engine)



app=FastAPI()



 
try:
    #For windows
    conn=psycopg2.connect(host='localhost',database='fastApi',user='postgres',password='3149',cursor_factory=RealDictCursor)
    # For Mac
    # conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='3149',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Succesfully Connected")
except Exception as error:
    print("Failled To connect with DB")
    print('Error',error)    

myUser=[{"id":1,"title":"Api title 1","content":"Api content 1"},{"id":2,"title":"Api title 2","content":"Api content 2"}]   

def checkId(id):
        
 for p in myUser:
     if p['id']== id:
         return p
         


def findPostForById(id):
    for i,p in enumerate(myUser):
        if p['id']==id:
            return i
          
          
app.include_router(post.router)          
app.include_router(user.router)     
app.include_router(auth.router)     
@app.get('/') 
async def root():
    return{"status":"Welcome To FastApI"} 



 
    