

from typing import Optional
from beanie import Document
from pydantic import BaseModel, ConfigDict


class Reviews(Document):
   user: Optional[str] = None
   park_name: str
   content: str
   rating: int
   upvotes: Optional[int] = 0 

   class Config: 
      json_schema_extra = {
         "example": {
            "user": "example@gmmail.com",
            "park_name": "Carlsbad",
            "content": "I loved it here. I recommend coming in the Summer when it is less windy and warm.",
            "rating": 5,
            "upvotes": 0
         }
      }


class UpdateReviews(BaseModel):
   # user: Optional[str] = None 
   # park_name: Optional[str] = None
   content: Optional[str] = None
   rating: Optional[int] = None
   # upvote: Optional[int] = None

   # Different approach of Config as seen above.
   model_config = ConfigDict(
      json_schema_extra= {
         "example": {
            "content": "Updated content.",
            "rating": 4 
         }
      }
   )