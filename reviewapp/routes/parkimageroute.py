import logging
from io import BytesIO
from fastapi.responses import JSONResponse, StreamingResponse
from auth.authenticate import authenticate
from models.parkimage import ParkImages
from typing import Dict, List, Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, File, FastAPI, UploadFile
from logging_setup import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

park_images_router = APIRouter(tags=["Park Images"])

@park_images_router.post("/upload-image/")
async def upload_image(user: str = Depends(authenticate), park_name: str = Query(..., description="The name of the park that is in the image."), file: UploadFile = File(..., description="Image file to upload to database.")):
    """Upload an image to the database."""
    logger.info(f"Uploading image for park: {park_name} by user: {user}")

    # Crucial in ensuring that the uploaded file is some sort of image (jpeg, png)
    if not file.content_type.startswith('image/'):
        logger.error("File provided is not an image.")
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_data = await file.read()
    logger.info("Reading image data from file.")

    new_image = ParkImages(user=user, park_name=park_name, image_data=image_data)
    logger.info("Creating new ParkImages object.")

    logger.info("Inserting image into the database...")
    await new_image.insert()
    logger.info("Image uploaded successfully.")

    return {"filename": file.filename, "message": "Image uploaded successfully!"}

@park_images_router.get("/images/{id}")
async def get_image(id: str = Path(..., description="ID of the image you want to retrieve.")):
    logger.info(f"Retrieving image with ID: {id}")
    image_record = await ParkImages.get(id)
    if not image_record:
        logger.error(f"Image with ID {id} not found.")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="ID does not exist in db.")

    logger.info("Returning image data as a streaming response.")
    return StreamingResponse(BytesIO(image_record.image_data), media_type="image/jpeg")

@park_images_router.get("/images/by-park/{park_name}")
async def get_images(park_name: str):
    logger.info(f"Retrieving images for park: {park_name}")
    image_record = await ParkImages.find(ParkImages.park_name == park_name).to_list()
    if not image_record:
        logger.error(f"No images found for park: {park_name}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No images")

    images_data = []
    for image in image_record:
        image_id = str(image.id)
        image_data = {
            "image_id": image_id,
            "url": f"/images/{image_id}"
        }
        images_data.append(image_data)

    logger.info(f"Found {len(images_data)} images for park: {park_name}")
    return images_data