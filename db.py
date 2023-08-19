from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Contact 
from typing import Optional
from datetime import datetime

SQLALCHEMY_DATABASE_URL='sqlite:///./contact.db'

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)


#To find all the primary contacts on the basis of given email and phonenumber
def get_primary_contact(email: Optional[str], phone_number: Optional[str]):
    session = SessionLocal()
    query = session.query(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phone_number),
        Contact.linkPrecedence == "primary"
    )
    contacts = query.all()

    primary_contact = None
    secondary_contact = None

    if len(contacts) == 2 and all(contact.linkPrecedence == "primary" for contact in contacts):
        # Determine the oldest primary contact and the other one
        primary_contact, secondary_contact = sorted(contacts, key=lambda x: x.createdAt)

        # Update the newer contact to be secondary and link it to the oldest
        secondary_contact.linkedId = primary_contact.id
        secondary_contact.linkPrecedence = "secondary"
        secondary_contact.updatedAt = datetime.utcnow()
        session.commit()
    

    if len(contacts)==1:
         primary_contact = contacts[0]
         return primary_contact

    if contacts is None and (email or phone_number):
        current_time = datetime.utcnow() 
        contact = Contact(
            email=email,
            phoneNumber=phone_number,
            linkedId="",
            linkPrecedence="primary",
            createdAt=current_time, 
            updatedAt=current_time  
        )
        session.add(contact)
        session.commit()
        session.refresh(contact)
        

    return primary_contact


#to find all the secondary contacts related to that primary contact
def get_secondary_contacts(primary_contact_id: int,email:Optional[str],phone_number:Optional[str]):
    session = SessionLocal()
    query = session.query(Contact).filter(Contact.linkedId == primary_contact_id)
    secondary_contacts = query.all()

    if not secondary_contacts and (email or phone_number):
        current_time = datetime.utcnow()
        secondary_contact = Contact(
            email=email,
            phoneNumber=phone_number,
            linkedId=primary_contact_id,
            linkPrecedence="secondary",
            createdAt=current_time,
            updatedAt=current_time
        )
        session.add(secondary_contact)
        session.commit()
        secondary_contacts = [secondary_contact]
    
    return secondary_contacts