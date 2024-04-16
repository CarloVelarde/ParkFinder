import os
from fastapi import APIRouter, HTTPException, status 
import httpx

from models.parks import Parks

park_routes_router = APIRouter(tags=["Database Queries"])



@park_routes_router.post("/parks/refresh-parks", status_code = status.HTTP_200_OK)
async def refresh_parks_data():

   API_URL = "https://developer.nps.gov/api/v1/parks"
   params = {
      "limit": 500,
      "fields": "fullName,parkCode,stateCode,description,activities,topics,states,contacts,entranceFees, operatingHours,addresses,images,weatherInfo"
   }
   headers = {
      "X-Api-Key": f"{os.getenv("NPS_KEY")}"
   }

   async with httpx.AsyncClient() as client:
      response = await client.get(API_URL, headers=headers, params=params)
      if response.status_code != 200:
         raise HTTPException(status_code=response.status_code, detail="NPS API call failed")
      
      parks_data = response.json()["data"]

      await Parks.delete_all()

      # for park in parks_data:
      #   new_park = Parks(
      #       park_name=park["fullName"],
      #       park_code=park["parkCode"]
      #   )
      #   await new_park.insert()
