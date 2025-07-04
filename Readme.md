# Park Finder

By: Kevin O'Connell, Carlo Velarde, and Gabe Solis

Group: Hawkeye Developers

## About

Discover a world of outdoor adventures with Park Finder, an intuitive app designed to provide comprehensive information on parks around you. With Park Finder, you no longer need to scour multiple websites or flip through guidebooks to find your next green getaway. Our mission was simple: consolidate all park-related information into one accessible location, giving you the freedom to explore nature with confidence.

To get started, you can search for a park by either state, park name, or both. Select the park you are interested in. After selection, you will be taken to a new page with information regarding that specific park. On the page there are two distinct feautures, one is you can view visitor uploaded photos. These are photos that other users have shared regarding the park. The other feauture is a review button. Click that button to be taken to a page of user reviews of that park. These reviews are extremely insightful as they provide a
unique and inside view of the park. Many users will talk about what they did, what they saw, where they went, and offer general advice. Those type of reviews can help determine whether that park is right for you. 

Any visitor, guest or signed user, is able to view the parks, the user uploaded images, and the user reviews. However, only signed in users can upload images and write reviews. Only the author of the review is able to edit and delete the review.


## Setup
#### Clone the Repo

#### Create Virtual Enviroment

`python -m venv venv`

#### Activating virtual enviroment

* For __mac__
   `source venv/bin/activate`

* For __windows__
   `.\venv\Scripts\activate`


*When the virtual enviroment is installed and activated please install the requirements with the code below.*

#### Requirements code

`pip install -r requirements.txt`

#### Create .env file
Create three fiels: __NPS_KEY__, __ADMIN_CODE__, and __DB_CONN__
* Give __NPS_KEY__ an API code from this website: `https://www.nps.gov/subjects/developer/get-started.htm`
* Give __ADMIN_CODE__ a secure random numbers for managing secrets (32 bit)
   * Using the tokens library do `token_hex(32)`
   * Sample key you can use: "2f555d823244910d10c9cab9f53bda040d33820be75f50f62a816106bac2da43"
   * The key is used to give admin privalages on user sign up.
* Give __DB_CONN__ a mongodb connection string.


### Run Program

After each step has been completed, using an IDE run the program from the main.py file or enter in a terminal `python main.py`

A link will be displayed in the terminal and click it `http://127.0.0.1:8000`

*__VERY IMPORTANT__ when you load up the link, go to the /docs endpoint and run the /parks/refresh-parks/ endpoint. Necessary to load database with parks.*
   * *Only need to do this once. The database will be saved for the next time you run it.*
   * Out of the box, this endpoint is locked to admins only. There are two solutions:
        * Create an admin account by passing in the ADMIN_CODE *(see above)* when doing the sign up feauture in the swagger docs. Once you sign up and authorize, call the endpoint.
        * Remove the authorization from that specific endpoint. Go to the parkroutes.py file in routes and edit it.


## Snapshots of Website

### Park Home Page

<img width="1318" alt="Screen Shot 2024-04-29 at 5 56 17 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/d6159fec-cd29-4d9d-bb1c-4c566a14969d">

### Park About Page

<img width="1318" alt="Screen Shot 2024-04-29 at 5 57 05 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/1c28d8ec-f957-481e-aca1-eec51fb43d4f">

<img width="1322" alt="Screen Shot 2024-04-29 at 5 57 24 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/f1b3d464-8e14-4d36-a0cd-212cc377d3c4">

### Park Search Page

<img width="1313" alt="Screen Shot 2024-04-29 at 5 59 17 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/2c864599-0567-4ce3-8048-fe023ada7ad0">

### Park Search Example

<img width="1315" alt="Screen Shot 2024-04-29 at 6 00 00 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/c6c4102b-ddf6-4126-b93f-4cf858b087c9">

### Park Page Example

<img width="1317" alt="Screen Shot 2024-04-29 at 6 00 51 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/eb735ecc-0377-46c6-8e2a-0e23c7c038c4">

### Park Page Review Example

<img width="1315" alt="Screen Shot 2024-04-29 at 6 02 20 PM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/cefc7ace-65fd-4bbf-af2a-f09b60dd37ba">

### Review Post Modal

<img width="547" alt="Screen Shot 2024-04-30 at 8 31 29 AM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/ac967bbc-7db3-4004-943e-bd73c270bbc5">

### Fast API Docs

<img width="1316" alt="Screen Shot 2024-04-30 at 8 33 34 AM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/72d53c67-0256-4811-a306-279a6d0ec602">

<img width="1309" alt="Screen Shot 2024-04-30 at 8 33 53 AM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/a2e81f22-78e2-4dbb-b900-73b7d557277c">

<img width="1302" alt="Screen Shot 2024-04-30 at 8 34 12 AM" src="https://github.com/CarloVelarde/ParkFinder/assets/45603150/ff089a66-9880-47f9-a005-2736e5c410c8">
