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

// Build park page
function buildSearchArea(parks){
   park_results_row.innerHTML = "";

   parks.forEach((park, index) =>{
      let park_name = park.park_name.trim()
      let park_image = park.images[0]
      let state_code = park.state_code

      park_results_row.innerHTML += `
      <div class="col-xl-3 col-lg-4 col-md-6 col-sm-12 d-flex justify-content-sm-center">
         <div class="card" style="width: 18rem;">
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


   if (parks_by_names.length === 0){
      return parks_by_states
   }

   else if (parks_by_states.length === 0){
      return parks_by_names
   }
   else {
      let common_parks = findCommonParks(parks_by_states, parks_by_names)
      return common_parks
   }
}


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

})




