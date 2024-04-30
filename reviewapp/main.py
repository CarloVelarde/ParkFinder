import logging
from logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database.connection import init_db
from routes.parkreview import park_reviews_router
from routes.parkroutes import park_routes_router
from routes.parkimageroute import park_images_router
from routes.users import user_router

logger.info("Starting up the Park Finder API")

app = FastAPI(
    title="API for Park Finder Application",
    summary="An API for the Park Finder Application for Spring 2024 Web Application Course CS 3980."
)

# Initializes the connection.py file
async def startup():
    logger.info("Initializing database connection")
    await init_db()

# The index file becomes the root document
@app.get("/", tags=["Root"])
async def read_index():
    return FileResponse("../frontend/index.html")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", startup)

app.include_router(park_reviews_router, prefix="/reviews")

app.include_router(park_routes_router, prefix="/parks")

app.include_router(park_images_router)

app.include_router(user_router, prefix="/user")

app.mount("/", StaticFiles(directory="../frontend"), name="static")


if __name__ == "__main__":
    logger.info("Starting the server")
    uvicorn.run("main:app", reload=True)