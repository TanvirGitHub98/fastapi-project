from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db
from fastapi import  Depends, HTTPException, Response,status,APIRouter
from typing import List


router=APIRouter(
    tags=['Posts']
)

@router.get('/getAllPosts',response_model=List[schemas.Postresponse])
async def getPosts(db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()
    
    #using orm alchemy
    posts=db.query(models.Post).all()
    return posts

@router.post('/createPost',status_code=status.HTTP_201_CREATED,response_model=schemas.Postresponse)
async def createPost(post:schemas.Postcreate,db:Session=Depends(get_db)):
#    cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
#    new_post=cursor.fetchone()
#    conn.commit()

   #new_post=models.Post(title=post.title, content=post.content, published=post.published)#this line we can make short, lets see
   new_post=models.Post(**post.model_dump())# This is the shorter version
   db.add(new_post)
   db.commit()
   db.refresh(new_post)  #returns the new created post
   return new_post
   
  
    
@router.get('/postgetById/{id}',response_model=schemas.Postresponse)
async def postGetById(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE ID=%s """,(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id :{id} not found")
        
    return post
    
    
    
@router.delete('/deletePostById/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id:int,db:Session=Depends(get_db)):
    
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User Id: {id} Not Found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        

@router.put('/updatePostById/{id}',response_model=schemas.Postresponse)
async def updatePost(id:int,post:schemas.Postcreate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET  title=%s, content=%s,published=%s  WHERE ID=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_Post=cursor.fetchone()
    # conn.commit()
    
    updated_query=db.query(models.Post).filter(models.Post.id==id)
    Updated_post=updated_query.first()
    
    if Updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Id {id} is not available")
    
    updated_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return updated_query.first()