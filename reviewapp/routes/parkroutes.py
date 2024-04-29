import os
from typing import Dict, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
import httpx
import re
import logging

from auth.authenticate import authenticate
from models.parks import Parks
from models.users import User

park_routes_router = APIRouter(tags=["Database Queries"])

# Set up the logger
logger = logging.getLogger(__name__)

@park_routes_router.post("/refresh-parks", status_code=status.HTTP_200_OK)
async def refresh_parks_data(user: User = Depends(authenticate)) -> Dict[str, str]:
    logger.info("Refreshing parks data")

    user = await User.find_one(User.email == user)
    if not (user.code == os.getenv("ADMIN_CODE")):
        logger.warning("Unauthorized user attempted to refresh parks data")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: You do not have the necessary permissions to refresh parks data.",
        )

    API_URL = "https://developer.nps.gov/api/v1/parks"
    params = {
        "limit": 500,
        "fields": "fullName,parkCode,stateCode,description,activities,topics,states,contacts,entranceFees, operatingHours,addresses,images,weatherInfo"
    }
    headers = {
        "X-Api-Key": f"{os.getenv('NPS_KEY')}"
    }

    async with httpx.AsyncClient() as client:
        logger.info("Sending request to NPS API")
        response = await client.get(API_URL, headers=headers, params=params)
        if response.status_code != 200:
            logger.error(f"NPS API call failed with status code {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="NPS API call failed")

        parks_data = response.json()["data"]

        await Parks.delete_all()
        logger.info("Deleted all existing parks from the database")

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

            # Images
            image_list = []
            image_data = park["images"]
            for item in image_data:
                image_list.append(item["url"])

            new_park = Parks(
                park_name=park["fullName"],
                park_code=park["parkCode"],
                state=park["states"],
                state_code=park["addresses"][0]["stateCode"],
                description=park["description"],
                activities=activity_list,
                topics=topic_list,
                contacts=contact_dict,
                fees=park["entranceFees"],
                operating_hours=operating_hours_dict,
                operating_hours_desc=operating_hour_desc,
                address=addresses_dict,
                images=image_list,
                weather=park["weatherInfo"]
            )
            await new_park.insert()

    logger.info("Successfully refreshed parks data")
    return {"Success": "updated all parks in database"}

@park_routes_router.get("/{id}", response_description="Get a park by ID.")
async def get_park_by_id(id: str = Path(..., description="id of the park you want to retrieve.")):
    """
    Get a park by ID.
    """
    logger.info(f"Retrieving park with ID: {id}")
    object_id = ObjectId(id)
    park = await Parks.find_one(Parks.id == object_id)
    if park:
        logger.info(f"Found park: {park.park_name}")
        return park
    else:
        logger.warning(f"Park with ID {id} not found")
        raise HTTPException(status_code=404, detail=f"Park {id} not found.")

@park_routes_router.get("/by-state/{state_code}", response_description="Find parks by state code.")
async def find_parks_by_state(state_code: str = Path(..., description="Code that represents specified state.")):
    """
    Retrieve all parks located in the specified state code.
    """
    logger.info(f"Retrieving parks in state: {state_code}")
    parks = await Parks.find_many(Parks.state_code == state_code.upper()).to_list()

    if parks:
        logger.info(f"Found {len(parks)} parks in state {state_code}")
        return parks
    else:
        logger.warning(f"No parks found in state {state_code}")
        raise HTTPException(status_code=404, detail=f"No parks with specified ID")

@park_routes_router.get("/by-name/{park_name}")
async def find_parks_by_name(park_name: str = Path(..., description="Name of the park you are searching for")):
    """
    Retrieve park(s) by name. Finds any parks where its name
    contains the given park_name parameter anywhere within it. Case-insensitive.
    """
    logger.info(f"Searching for parks with name containing: {park_name}")
    park_name = park_name.title()
    regex_pattern = re.compile(f".*{re.escape(park_name)}.*", re.IGNORECASE)
    parks = await Parks.find({"park_name": regex_pattern}).to_list()

    if parks:
        logger.info(f"Found {len(parks)} parks matching the search query")
    else:
        logger.warning(f"No parks found matching the search query: {park_name}")

    # Returns a list whether it finds something or not.
    return parks