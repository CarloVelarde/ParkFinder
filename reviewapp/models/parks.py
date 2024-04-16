from beanie import Document
from typing import Dict, List, Optional

class Parks(Document):
   park_name: str
   park_code: str
   # state: str
   # state_code: str
   # description: str
   # activities: List[str]
   # topics: List[str]
   # contacts: Dict[str, str] 
   # fees: List[str]   # probably will just do entrance fees
   # operating_hours: Dict[str, str]
   # operating_hours_desc: str
   # address: Dict[str, str]
   # images: List[str]
   # weather: str

   class Settings:
      name = "Parks"


   

   # class Config: 
   #    json_schema_extra = {
   #       "example": {
   #          "park_name": "Carlsbad Caverns",
   #          "state": "New Mexico",
   #          "address": "3225 National Park Hwy",
   #          "images": ["http.image.com"]
   #       }
   #    }