from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from database.connection import init_db

from routes.parkreview import park_reviews_router
from routes.parkroutes import park_routes_router
from routes.parkimageroute import park_images_router

app = FastAPI(
   title = "API for Park Finder Application",
   summary = "An API for the Park Finder Application for Spring 2023 Web Application Course CS 3980."
)

# Initializes the connection.py file
async def startup():
   await init_db()



# The index file becomes the root document
@app.get("/", tags = ["Root"])
async def read_index():
   return FileResponse("../frontend/index.html")

app.add_event_handler("startup", startup)
app.include_router(park_reviews_router)
app.include_router(park_routes_router)
app.include_router(park_images_router)


app.mount("/", StaticFiles(directory = "../frontend"), name = "static")
# Ask professor if I should make it static
# app.mount("/static", StaticFiles(directory = "../frontend"), name = "static")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)