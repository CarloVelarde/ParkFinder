import os
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Path

from auth.authenticate import authenticate
from models.reviews import Reviews, UpdateReviews
from models.users import User

# Still need to add queery and path descriptions and more type checking.



park_reviews_router = APIRouter(tags=["Park Reviews"])

# Get all reviews
@park_reviews_router.get(
   "/",
   response_description="List all reviews",
)
async def get_reviews():
   """
   List all the reviews in the review collection.
   """
   reviews = await Reviews.find().to_list()
   return reviews


# Get a single review
@park_reviews_router.get(
   "/{id}",
   response_description="Get a single review by ID",
)
async def get_review_by_id(id: str):
   """
   Get a review by ID.
   """
   review = await Reviews.find_one({"_id": ObjectId(id)})
   if review: 
      return review 
   
   raise HTTPException(status_code=404, detail=f"Review {id} not found")

# Get all reviews for a certain state
# Still not final... Make sure the type checking for state parameter is good.
@park_reviews_router.get(
   "/parks/{park}",
   response_description="Get all reviews for a certain park",
)
async def get_reviews_by_park(park: str):
   """
   Get reviews under a specific park.
   """
   reviews = await Reviews.find(Reviews.park_name == park).to_list()
   return reviews


# Post a review
@park_reviews_router.post(
   "/post/",
   response_description= "Add a new review to the db.",
   status_code = status.HTTP_201_CREATED,
)
async def post_review(review: Reviews, user: str = Depends(authenticate)):
   """
   Create a review and post it to the db.
   """
   review.user = user
   await Reviews.insert(review)
   return review



@park_reviews_router.delete(
   "/delete/{id}",
   response_description= "Delete a review from the database by ID.",
   status_code = status.HTTP_202_ACCEPTED,
)
async def delete_review(user: str = Depends(authenticate), id: str = Path(..., description = "ID of the review you want to delete from the db.")):
   """
   Remove a single review from the db.
   """
   object_id = ObjectId(id)
   review = await Reviews.find_one(Reviews.id == object_id)
   user_account = await User.find_one(User.email == user)
   if not (user_account.code == os.getenv("ADMIN_CODE") or user == review.user):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operation not allowed")
   if review:
      await review.delete()
      return review
   if not review:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
      detail = f"Review {id} not found.")

   




@park_reviews_router.put(
   "/update/{id}",
   response_description= "Update a review in the db.",
   status_code = status.HTTP_200_OK,
)
async def update_review(id: str, updateReview: UpdateReviews, user: str = Depends(authenticate)):
   """
   Update a review with given body.
   """
   object_id = ObjectId(id)
   review = await Reviews.find_one(Reviews.id == object_id)
   user_account = await User.find_one(User.email == user)
   if not (user_account.code == os.getenv("ADMIN_CODE") or user == review.user):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operation not allowed")

   if review:
      if updateReview.content:
         review.content = updateReview.content   

      if updateReview.rating:
         review.rating = updateReview.rating
      
      await review.save()
      return review
   else:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Review {id} not found")
