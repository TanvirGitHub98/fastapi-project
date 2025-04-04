from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time

DATABASE_URL = "postgresql://postgres:3149@localhost/fastApi"
# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define the base class for models
Base = declarative_base()



#help to get session/connection to database

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
   
 #Without orm(alchemy) db con       
# while True:        

#     try:
#         #For windows
#         conn=psycopg2.connect(host='localhost',database='fastApi',user='postgres',password='3149',cursor_factory=RealDictCursor)
#         # For Mac
#         # conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='3149',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Succesfully Connected")
#         break
#     except Exception as error:
#         print("Failled To connect with DB")
#         print('Error',error)   
#         time.sleep(2)         