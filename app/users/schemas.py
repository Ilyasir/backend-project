from pydantic import BaseModel, EmailStr

class SUserReg(BaseModel):
    username: str
    email: EmailStr
    password: str

class SUserAuth(BaseModel):
    email: EmailStr
    password: str