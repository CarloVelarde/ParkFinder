from beanie import Document
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(Document):
    email: EmailStr = ""
    password: str = ""
    code: str = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "grsolis@uiowa.edu", "password": "1234", "code": "p1i4432ufbh4cr3q4"}
        }
    )

    class Settings:
        name = "users"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str