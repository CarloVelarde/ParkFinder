import os
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Path
from auth.authenticate import authenticate
from models.reviews import Reviews, UpdateReviews
from models.users import User
import logging

logger = logging.getLogger(__name__)

# Still need to add queery and path descriptions and more type checking.
park_reviews_router = APIRouter(tags=["Park Reviews"])

# Get all reviews
@park_reviews_router.get(
    "/", response_description="List all reviews",
)
async def get_reviews():
    logger.info("Retrieving all reviews")
    """ List all the reviews in the review collection. """
    reviews = await Reviews.find().to_list()
    logger.info(f"Found {len(reviews)} reviews")
    return reviews

# Get a single review
@park_reviews_router.get(
    "/{id}", response_description="Get a single review by ID",
)
async def get_review_by_id(id: str):
    logger.info(f"Retrieving review with ID: {id}")
    """ Get a review by ID. """
    review = await Reviews.find_one({"_id": ObjectId(id)})
    if review:
        logger.info(f"Found review: {review.content[:20]}...")
        return review
    logger.warning(f"Review with ID {id} not found")
    raise HTTPException(status_code=404, detail=f"Review {id} not found")

# Get all reviews for a certain state
# Still not final... Make sure the type checking for state parameter is good.
@park_reviews_router.get(
    "/parks/{park}", response_description="Get all reviews for a certain park",
)
async def get_reviews_by_park(park: str):
    logger.info(f"Retrieving reviews for park: {park}")
    """ Get reviews under a specific park. """
    reviews = await Reviews.find(Reviews.park_name == park).to_list()
    logger.info(f"Found {len(reviews)} reviews for park: {park}")
    return reviews

# Post a review
@park_reviews_router.post(
    "/post/", response_description="Add a new review to the db.", status_code=status.HTTP_201_CREATED,
)
async def post_review(review: Reviews, user: str = Depends(authenticate)):
    logger.info(f"User [{user}] is posting a new review")
    """ Create a review and post it to the db. """
    review.user = user
    await Reviews.insert(review)
    logger.info(f"Review posted: {review.content[:20]}...")
    return review

@park_reviews_router.delete(
    "/delete/{id}", response_description="Delete a review from the database by ID.", status_code=status.HTTP_202_ACCEPTED,
)
async def delete_review(user: str = Depends(authenticate), id: str = Path(..., description="ID of the review you want to delete from the db.")):
    logger.info(f"User [{user}] is attempting to delete review with ID: {id}")
    """ Remove a single review from the db. """
    object_id = ObjectId(id)
    review = await Reviews.find_one(Reviews.id == object_id)
    user_account = await User.find_one(User.email == user)
    if not user_account:
        logger.warning(f"User [{user}] is not authorized to delete review with ID: {id}")
    if not (user_account.code == os.getenv("ADMIN_CODE") or user == review.user):
        logger.warning(f"User [{user}] is not authorized to delete review with ID: {id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operation not allowed")
    if review:
        logger.info(f"Deleting review with ID: {id}")
        await review.delete()
        logger.info(f"Review with ID: {id} deleted successfully")
        return review
    if not review:
        logger.warning(f"Review with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review {id} not found.")

@park_reviews_router.put(
    "/update/{id}", response_description="Update a review in the db.", status_code=status.HTTP_200_OK,
)
async def update_review(id: str, updateReview: UpdateReviews, user: str = Depends(authenticate)):
    logger.info(f"User [{user}] is attempting to update review with ID: {id}")
    """ Update a review with given body. """
    object_id = ObjectId(id)
    review = await Reviews.find_one(Reviews.id == object_id)
    user_account = await User.find_one(User.email == user)
    if not (user_account.code == os.getenv("ADMIN_CODE") or user == review.user):
        logger.warning(f"User [{user}] is not authorized to update review with ID: {id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operation not allowed")
    if review:
        if updateReview.content:
            review.content = updateReview.content
            logger.info(f"Updating review content for review with ID: {id}")
        if updateReview.rating:
            review.rating = updateReview.rating
            logger.info(f"Updating review rating for review with ID: {id}")
        await review.save()
        logger.info(f"Review with ID: {id} updated successfully")
        return review
    else:
        logger.warning(f"Review with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review {id} not found")