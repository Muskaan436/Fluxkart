from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from db import get_primary_contact, get_secondary_contacts,engine
from schemas import IdentifyRequest,Contact,IdentifyResponse
import models


app=FastAPI()
 

models.Base.metadata.create_all(bind=engine)


@app.post("/identify", response_model=IdentifyResponse)
async def identify_contact(request: IdentifyRequest) -> IdentifyResponse:
    primary_contact = get_primary_contact(request.email, request.phoneNumber)
    
    secondary_contacts = get_secondary_contacts(primary_contact.id,request.email,request.phoneNumber)

    


        
    

    contact = Contact(
        primaryContatctId=primary_contact.id,
        emails=[primary_contact.email] + [sec.email for sec in secondary_contacts if sec.email!=primary_contact.email],
        phoneNumbers=[primary_contact.phoneNumber] + [str(sec.phoneNumber) for sec in secondary_contacts if sec.phoneNumber!=primary_contact.phoneNumber],
        secondaryContactIds=[sec.id for sec in secondary_contacts]
    )

    return {"contact": contact}



