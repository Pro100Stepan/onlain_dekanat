from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import base64

from pydantic.types import ByteSize






class UserBase(BaseModel):
   # id: int
    login: str
    email: str 
    phone: str
    role: str 
    name: str 
    admission_year: str 
    course: Optional[int] 
    direction: Optional[str] 
    group: Optional[str]
    hostel: Optional[str] 
    password: Optional[str]
    zachetkaid: Optional[str]
    
class UserCreate(UserBase):
   # id: int
    login: str
    email: str 
    phone: str
    role: str 
    name: str 
    admission_year: str 
    course: Optional[int] 
    direction: Optional[str] 
    group: Optional[str]
    hostel: Optional[str] 
    password: Optional[str]
    zachetkaid: Optional[str] 
class UserUpdate(UserBase):
    pass

#DATABASE BASE
class User(UserBase):
    #id: int
    login: str
    email: str 
    phone: str
    role: str 
    name: str 
    admission_year: str 
    course: Optional[int] 
    direction: Optional[str] 
    group: Optional[str]
    hostel: Optional[str] 
    password: Optional[str]
    zachetkaid: Optional[str] 
   
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class MessageBase(BaseModel):
    sender_1: int
    sender_2: int
    Messages: dict

class Message(MessageBase):
    sender_1: int
    sender_2: int
    Messages: dict
