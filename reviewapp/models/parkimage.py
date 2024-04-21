from beanie import Document
from typing import Any, Dict, List, Optional

class ParkImages(Document):
   user: str
   park_name: str
   image_data: bytes


