from pydantic import BaseModel
from typing import Optional,List

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class Contact(BaseModel):
    primaryContatctId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]


class IdentifyResponse(BaseModel):
    contact: Contact
