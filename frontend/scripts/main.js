const API = "http://127.0.0.1:8000/"


// Parks search form
let state_selector = document.getElementById("select-state")
let search_input = document.getElementById("search-text-input")
let search_button = document.getElementById("search-parks-button")


// Area to display parks
let park_results_area = document.getElementById("park-results-container")
let park_results_row = document.getElementById("park-results-row")


// Returns parks by state given state_id
async function fetchParksByState(state_id){
   try {
      const response = await fetch(API + `parks/by-state/${state_id}`)
      if (!response){
         throw new Error ("Could not fetch resource")
      }

      const data = await response.json()
      return data
   }
   catch(error) {
      console.error(error)
   }
}

// Returns a park given the id
async function fetchParkByID(id){
   try {
      const response = await fetch(API + `parks/${id}`)
      if (!response){
         throw new Error ("Could not fetch resource")
      }

      const data = await response.json()
      return data
   }
   catch(error) {
      console.error(error)
   }
}

// Returns parks by parkname given park_name
async function fetchParksByName(park_name){
   try {
      const response = await fetch(API + `parks/by-name/${park_name}`)
      if (!response){
         throw new Error ("Could not fetch resource")
      }

      const data = await response.json()
      return data
   }
   catch(error) {
      console.error(error)
   }
}

async function fetchUserImagesByName(park_name){
   try {
      const response = await fetch(API + `images/by-park/${park_name}`)
      if (!response){
         throw new Error ("Could not fetch resource")
      }

      const data = await response.json()
      return data
   }

   catch(error){
      console.error(error)
      return []
   }
}

async function fetchUserImagesById(id){
   try {
      const response = await fetch(API + `images/${id}`)
      if (!response){
         throw new Error ("Could not fetch resource")
      }

      const data = response.blob()
      return data
   }
   
   catch (error){
      console.error(error)
   }
}

async function uploadFile(user, parkName, fileInput) {
   if (fileInput.files.length > 0) {
       const file = fileInput.files[0];

       const formData = new FormData();
       formData.append('file', file);

       const url = new URL(API + 'upload-image/');
       url.searchParams.append('user', user);
       url.searchParams.append('park_name', parkName);

       try {
           const response = await fetch(url, {  // Using constructed URL with query params
               method: 'POST',
               body: formData,
           });

           if (!response.ok) {
               throw new Error('Failed to upload image: ' + await response.text());
           }

           const result = await response.json();
           alert('Success: ' + result.message)

           return true;
            
       } catch (error) {
           console.error('Error:', error);
           alert('Error: ' + error.message);
           return false
           
       }
   } else {
      alert('Please select a file to upload.')
      return false;
   }
}

// Build park page
function buildSearchArea(parks){
   park_results_row.innerHTML = "";

   parks.forEach((park, index) =>{
      let park_name = park.park_name.trim();
      let park_image = park.images[0];
      let state_code = park.state_code;
      let park_id = park._id;

      park_results_row.innerHTML += `
      <div class="col-xl-3 col-lg-4 col-md-6 col-sm-12 d-flex justify-content-sm-center park-card" data-park-id="${park_id}">
         <div class="card park-search-card" style="width: 18rem;">
            <img src="${park_image}" class="card-img-top" alt="picture of ${park_name}" style = "width:100%;height:200px;object-fit:cover;">
            <div class="card-body">
               <h5 class="text-center">${park_name}</h5>
            </div>
         </div>
      </div>
      `
   })
}





// Takes two lists of parks and return a list of the common (overlapping)
// parks. 
function findCommonParks(list1, list2) {
   let commonParks = [];
   let parkNameSet = new Set(list2.map(park => park.park_name));

   list1.forEach(park => {
       if (parkNameSet.has(park.park_name)) {
           commonParks.push(park);
       }
   });

   return commonParks;
}

// Given state id and name (think of them as fields), it will search for
// all parks that match the given state and name.
// Returns a list of matching parks.
async function searchParksByInput(state_id, state_name){
   parks_by_names = []
   parks_by_states = []

   // Check if there is at least a state id or state name
   if (!(state_id || state_name)){
      return
   }

   // Check if given a state name
   if (state_name.length > 0){
      parks_by_names = await fetchParksByName(state_name)
   }

   // Checks if given a state id
   if (state_id){
      parks_by_states = await fetchParksByState(state_id)
   }

   if (state_id && !(state_name)){
      return parks_by_states
   }

   // if there was a search and nothing showed up, return nothing
   else if (parks_by_names.length === 0 && parks_by_states.length > 1){
      return []
   }

   else if (parks_by_states.length === 0){
      return parks_by_names
   }
   else {
      let common_parks = findCommonParks(parks_by_states, parks_by_names)
      return common_parks
   }
}

// Adds an event listener to each card on the parks.html page
function setupParkCards(){
   const cards = document.querySelectorAll('.park-card');
   cards.forEach(card => {
      card.addEventListener('click', function (){
         const parkId= card.getAttribute('data-park-id');
         localStorage.setItem('selectedParkId', parkId);
         window.location.href = 'park-details.html'
      });
   });
}


// Sets up the parks.html page with appropiate event listeners and
// functionality.
function initializeParksPage(){

   // When the user clicks on the search button, the eventlistener will 
   // query the database and display what is found.
   search_button.addEventListener("click", async () => {
      // Checks if there is input before searching. 
      // If there is not, it terminates the function.
      let state_id = state_selector.value
      let state_name = search_input.value.trim()
      if (!(state_id || state_name)){
         return
      } 

      let parks = await searchParksByInput(state_id, state_name)
      buildSearchArea(parks)
      setupParkCards() // This adds an event listener to each newly created card.
   })
}


// Given a list of picture urls, it gets image and if none exist, then return none.
// If there is an image, it returns it and then removes from array.
function getRandomImageAndRemove(pictures) {
   if (pictures.length === 0) {
       throw new Error("No pictures available");
   }
   const index = Math.floor(Math.random() * pictures.length);
   return pictures.splice(index, 1)[0]; // Removes the image from the array and returns it
}

function buildAddress(park){
   let addy = park.address;
   const new_addy = addy.line1 + " " + addy.city + ", " + addy.stateCode + " " + addy.countryCode + ", " + addy.postalCode
   return new_addy
}

// Helper method that builds the image slider given an array of image links
function buildSlider(userImages) {
   let section = ``;
   userImages.forEach((image, index) => {
       section += `
       <div class="carousel-item ${index === 0 ? 'active' : ''}">
           <img src="${image}" class="d-block w-100" alt="User uploaded image">
       </div>
       `;
   });
   return section;
}


// Given park name, it will return a list of all user uploaded images (as urls) by given park
async function getUserImages(park_name){

   let imageArray = []
   let imageData = await fetchUserImagesByName(park_name)
   
   if (imageData && imageData.length > 0){
      for (let image of imageData) {
         const imgBlob = await fetchUserImagesById(image.image_id);  // Fetch the image blob using the image ID
         if (imgBlob) {
             const imgURL = URL.createObjectURL(imgBlob);  // Create a local URL to be used in an <img> element
             imageArray.push(imgURL);
         }
     }
   }
   return imageArray
}


// Displays park data in park-details.html
async function displayParkData(){
   const parkId = localStorage.getItem('selectedParkId');
   
   

   let park = await fetchParkByID(parkId);
   
   let userImages = await getUserImages(park.park_name);
   let section = buildSlider(userImages)
   

   let park_images = park.images;
   const topics = park.topics.slice(0,7).join(", ");
   const address = buildAddress(park);

   let docu = document.getElementById("details-park-body")
   
   docu.innerHTML += `

   <!-- Heading -->
   <section class="bg-dark text-light p-5 p-lg-0 pt-lg-5 text-center text-sm-start">
      <div class="container">
         <div class = "d-sm-flex align-items-center justify-content-between" id="park-heading-container">
            <div class = "p-5">
               <h1>${park.park_name}</h1>
               <p><strong>Topics</strong>: ${topics}</p>
               
            </div>
            <img class = "img-fluid w-50 d-none d-sm-block p-5" src="${getRandomImageAndRemove(park_images)}" alt="">
         </div>
      </div>
   </section>

   <!-- Contact and View Reviews -->
   <section class = "pt-2 pb-2">
      <div class="container">
         <div class="row g-4 align-items-start mt-3 mb-3">
            <div class="col-md me-md-3">
               <ul class="list-group list-group-flush lead">
                  <li class="list-group-item">
                     <span class="fw-bold">Address: </span>${address}
                  </li>
                  <li class="list-group-item">
                     <span class="fw-bold">Phone:</span> ${park.contacts.phoneNumbers}
                  </li>
                  <li class="list-group-item">
                     <span class="fw-bold">Email: </span>${park.contacts.emailAddresses}
                  </li>
               </ul>
            </div>
            <div class="col-md-3 ms-md-4 ps-3 text-center">
               <h4> View User Reviews <i class="fa-solid fa-star text-warning"></i><i class="fa-solid fa-star text-warning"></i><i class="fa-solid fa-star text-warning"></i></h4>
               <button id = "viewReviewsButton" data-park-name="${park.park_name}" class = "btn btn-warning btn-lg mt-2">View Reviews</button>
            </div>
         </div>
      </div>
   </section>

   <!-- About -->
   <section class = "p-5 bg-dark text-light" id = "learn">
      <div class="container">
         <div class="row align-items-center justify-content-between">
            <div class="col-md">
               <img src="${getRandomImageAndRemove(park_images)}" class = "img-fluid rounded" alt="Picture of park">
            </div>
            <div class="col-md p-5">
               <h2>About</h2>
               <p class = "lead">${park.description}</p>
               <a href="https://www.nps.gov/index.htm" target = "_blank" class="btn btn-light mt-3">
                  <i class="bi bi-chevron-right"></i>Read More
               </a>
            </div>
            
         </div>
      </div>
   </section>

   <section class = "p-5" id = "learn">
      <div class="container">
         <div class="row align-items-center justify-content-between">
            
            <div class="col-md p-5">
               <h2>Operating Hours</h2>
               <p class = "lead">Monday: ${park.operating_hours.monday}</p>
               <p class = "lead">Tuesday: ${park.operating_hours.tuesday}</p>
               <p class = "lead">Wednesday: ${park.operating_hours.wednesday}</p>
               <p class = "lead">Thursday: ${park.operating_hours.thursday}</p>
               <p class = "lead">Friday: ${park.operating_hours.friday}</p>
               <p class = "lead">Saturday: ${park.operating_hours.saturday}</p>
               <p class = "lead">Sunday: ${park.operating_hours.sunday}</p>
            </div>
            <div class="col-md">
               <img src="${getRandomImageAndRemove(park_images)}" class = "img-fluid rounded" alt="Picture of park">
            </div>
         </div>
      </div>
   </section>

   <section class = "p-5 bg-dark text-light" id = "weather-park">
      <div class="container">
         <div class="row align-items-center justify-content-between">
            <div class="col-md">
               <img src="./assets/imgs/weather.jpg" class = "img-fluid rounded" alt="Picture of sky" style = "width:100%;height:400px;object-fit:cover;">
            </div>
            <div class="col-md p-5">
               <h2>Weather</h2>
               <p class = "lead">${park.weather}</p>
            </div>
            
         </div>
      </div>
   </section>

   <!--Image Upload Section -->
   
   <section class = "p-5" id = "learn">
      <div class="container">
         <div class="row align-items-center justify-content-between">
            <div class="col-md p-5">
               <h2>Visitor Uploaded Images</h2>
               <p class = "lead">Here are some images of the park that have been uploaded by other visitors. These photos give real feeling to the park.</p>
               <p>We encourage all users to upload their photos of the park. It allows you to share your personal expierence while also giving others an inside look into the park.</p>
               <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#imageModal">
                  Upload Image
                </button>


                <div class="modal fade" id="imageModal" tabindex="-1">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h1 class="modal-title fs-5" id="imageModalLabel">Upload Image</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                      </div>
                      <div class="modal-body">
                        <input type="file" id = "imageSubmitInput" accept = "image/*">
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" id = "uploadImageButton"class="btn btn-dark">Upload</button>
                      </div>
                    </div>
                  </div>
                </div>

            </div>

            <div class="col-md">
               <div id="carouselExample" class="carousel slide">
                  <div class="carousel-inner" id = "imageSliderDiv">
                    ${section}
                  </div>

                  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                    <span class="visually-hidden">Previous</span>
                  </button>
                  <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                    <span class="visually-hidden">Next</span>
                  </button>
                </div>
            </div>
            
         </div>
      </div>
   </section> 
   
   `
   
   

   

   // This is for the uploading images
   // Change users on here when able.
   document.getElementById('uploadImageButton').addEventListener('click', async function() {
      
      const fileInput = document.getElementById("imageSubmitInput");
      const user = "Gabe";  // Example user, should be dynamically set
      const parkName = park.park_name;
  
      const success = await uploadFile(user, parkName, fileInput);
      if (success) {
          // Only close the modal if the upload was successful

          fileInput.value = ""
          const modalElement = document.getElementById('imageModal');
          const modalInstance = bootstrap.Modal.getInstance(modalElement);
          modalInstance.hide();
      }

      
  });

  document.getElementById("viewReviewsButton").addEventListener('click', () => {
      let btn = document.getElementById("viewReviewsButton");
      const parkName= btn.getAttribute('data-park-name');

      localStorage.setItem('selectedParkName', parkName);
      window.location.href = 'reviews.html';
  })

  


}



// When any page is loaded, this calls the appropiate methods.
document.addEventListener('DOMContentLoaded', function(){
   if (window.location.pathname.includes('parks.html')){
      initializeParksPage()
   }
   else if (window.location.pathname.includes('park-details.html')){
      displayParkData()
   }
})












// // When the user clicks on the search button, the eventlistener will 
// // query the database and display what is found.
// search_button.addEventListener("click", async () => {
//    // Checks if there is input before searching. 
//    // If there is not, it terminates the function.
//    let state_id = state_selector.value
//    let state_name = search_input.value.trim()

//    if (!(state_id || state_name)){
//       return
//    } 

//    let parks = await searchParksByInput(state_id, state_name)
//    buildSearchArea(parks)
//    setupParkCards() // This adds an event listener to each newly created card.
// })