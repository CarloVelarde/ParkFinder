from io import BytesIO
from fastapi.responses import JSONResponse, StreamingResponse
from models.parkimage import ParkImages
from typing import Dict, List, Annotated
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path, Query, status, File, FastAPI, UploadFile 


park_images_router = APIRouter(tags=["Park Images"])



@park_images_router.post("/upload-image/")
async def upload_image(user: str = Query(..., description="Name of the user who uploaded the image"), park_name:str = Query(..., description="The name of the park that is in the image."), file: UploadFile = File(..., description="Image file to upload to database.")):

   """
   Upload an image to the database.
   """
   
   # Crucial in ensuring that the uploaded file is some sort of image (jpeg, png)
   if not file.content_type.startswith('image/'):
      raise HTTPException(status_code=400, detail="File provided is not an image.")
   
   image_data = await file.read()  # Read image file as bytes

   new_image = ParkImages(user=user, park_name = park_name, image_data=image_data)
   await new_image.insert()  # Save the image in the database using Beanie

   return {"filename": file.filename, "message": "Image uploaded successfully!"}


@park_images_router.get("/images/{id}")
async def get_image(id: str = Path(..., description="ID of the image you want to retrieve.")):

   image_record = await ParkImages.get(id)

   if not image_record:
      raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "ID does not exist in db.")
   
   return StreamingResponse(BytesIO(image_record.image_data), media_type="image/jpeg")
   




@park_images_router.get("/images/by-park/{park_name}")
async def get_images(park_name: str):
   
   image_record = await ParkImages.find(ParkImages.park_name == park_name).to_list()

   if not image_record:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No images")
   
   images_data = []

   for image in image_record:
      image_id = str(image.id)
      image_data = {
         "id": image_id,
         "url": f"/images/{image_id}"
      }
      images_data.append(image_data)
      
   # return JSONResponse(content={"images": images_data})
   return images_data
   

