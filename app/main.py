from random import randrange
from fastapi import  FastAPI, HTTPException, Response,status
from fastapi.params import Body
from pydantic import BaseModel, Field
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
 
try:
    #For windows
    conn=psycopg2.connect(host='localhost',database='fastApi',user='postgres',password='3149',cursor_factory=RealDictCursor)
    # For Mac
    # conn=psycopg2.connect(host='localhost',database='fastApi',user='postgres',password='3149',cursor_factory=RealDictCursor)
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
          
    

@app.get('/')
async def root():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()
    return{"All Post":posts}

@app.post('/createPost',status_code=status.HTTP_201_CREATED)
async def createPost(post:Post):
   cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
   new_post=cursor.fetchone()
   conn.commit()
   return{
       "new_post":new_post
   }
  
    
@app.get('/postgetById/{id}')
async def postGetById(id:int):
    cursor.execute("""SELECT * FROM posts WHERE ID=%s """,(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id :{id} not found")
        return
    return{
        "Id":post
    }
    
    
@app.delete('/deletePostById/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id:int):
    
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User Id: {id} Not Found")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@app.put('/updatePostById/{id}')
async def updatePost(id:int,post:Post):
    cursor.execute("""UPDATE posts SET  title=%s, content=%s,published=%s  WHERE ID=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_Post=cursor.fetchone()
    conn.commit()
    
    if updated_Post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id {id} is not available")

    return {"message": "Post updated successfully", "updatedPost": updated_Post}

