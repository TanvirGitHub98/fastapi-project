from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Integer, Column, String
from sqlalchemy.sql.expression import null,text
class Post(Base):
    __tablename__="posts"
    
    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String,  nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, default=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))