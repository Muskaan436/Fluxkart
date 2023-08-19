from base import Base
from sqlalchemy import Column,Integer,String,DateTime

class Contact(Base):
    __tablename__='contact'
   

    id=Column(Integer,primary_key=True,index=True)
    phoneNumber=Column(String)
    email=Column(String)
    linkedId=Column(Integer)
    linkPrecedence=Column(String)
    createdAt=Column(DateTime)
    updatedAt=Column(DateTime)
