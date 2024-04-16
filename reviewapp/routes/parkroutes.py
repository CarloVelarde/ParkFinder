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

      # Go through each park
      for park in parks_data:
        
        # activity field
        activities = park["activities"]
        activity_list = [activity["name"] for activity in activities]

        # topics field
        topics = park["topics"]
        topic_list = [topic["name"] for topic in topics]

        # All for contact field
        contacts = park["contacts"]
        contact_dict = {}
        if contacts.get("phoneNumbers"):  
           contact_dict["phoneNumbers"] = str(contacts["phoneNumbers"][0]["phoneNumber"])  

        if contacts.get("emailAddresses"): 
           contact_dict["emailAddresses"] = contacts["emailAddresses"][0]["emailAddress"]
        

        # Operating hours field and desc
        operating_hours_desc = ""
        operating_hours_dict = {}
        operatingHours = park["operatingHours"]
        if len(operatingHours) >= 1:
           standardHours = operatingHours[0]["standardHours"]
           operating_hour_desc = operatingHours[0]["description"]
           for day in standardHours:
              operating_hours_dict[day] = standardHours[day]

        # Address field
        addresses_dict = {}
        addresses = park["addresses"]
        if addresses[0]:
           for key in addresses[0]:
              addresses_dict[key] = addresses[0][key]
      

        #Images
        image_list = []
        image_data = park["images"]
        for item in image_data:
           image_list.append(item["url"])
        
        new_park = Parks(
           park_name=park["fullName"],
           park_code=park["parkCode"],
           state = park["states"],
           state_code = park["addresses"][0]["stateCode"],
           description = park["description"],
           activities = activity_list,
           topics = topic_list,
           contacts = contact_dict,
           fees = park["entranceFees"],
           operating_hours = operating_hours_dict,
           operating_hours_desc = operating_hour_desc,
           address = addresses_dict,
           images = image_list,
           weather = park["weatherInfo"]
        )
        await new_park.insert()
      
      return {"Success": "updated all parks in database"}

