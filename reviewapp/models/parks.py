from beanie import Document
from typing import List, Optional

class Parks(Document):
   park_name: str
   state: str
   address: str
   images: List[str]
   fees_passes: Optional[str] = None
   campgrounds: List[str]
   amenities: List[str]
   alerts: List[str]
   activities: List[str]

   # class Config: 
   #    json_schema_extra = {
   #       "example": {
   #          "park_name": "Carlsbad Caverns",
   #          "state": "New Mexico",
   #          "address": "3225 National Park Hwy",
   #          "images": ["http.image.com"]
   #       }
   #    }