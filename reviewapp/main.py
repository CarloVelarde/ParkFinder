from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database.connection import init_db

from routes.parkreview import park_reviews_router


app = FastAPI(
   title = "API for Park Finder Application",
   summary = "An API for the Park Finder Application for Spring 2023 Web Application Course CS 3980."
)

# Initializes the connection.py file
async def startup():
   await init_db()



# The index file becomes the root document
@app.get("/")
async def read_index():
   return FileResponse("../frontend/index.html")

app.add_event_handler("startup", startup)
app.include_router(park_reviews_router, tags = ["Park Reviews"])


app.mount("/", StaticFiles(directory = "../frontend"), name = "static")
# Ask professor if I should make it static
# app.mount("/", StaticFiles(directory = "../frontend"), name = "static")
