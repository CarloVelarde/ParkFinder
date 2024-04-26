const API = "http://127.0.0.1:8000/"

let review_container = document.getElementById("review-container")


let page_title = document.getElementById("page-title")
let page_address = document.getElementById("page-address")
let page_number = document.getElementById("page-number")
let heading_background = document.getElementById("heading-review-section")


let post_modal = document.getElementById("postModal")
let postReviewButton = document.getElementById("postReviewButton")

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


// Post reviews to database
async function postReview(user, park_name, content, rating){
   try {
      const data = {
         user: user,
         park_name: park_name,
         content: content,
         rating: rating
      };

      const response = await fetch(API + "reviews/post/",{
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify(data),
      });

      const result = await response.json()
      console.log("Success: ", result)
   }
   catch(error){
      console.error("Error:", error);
   }
}


// Fetch and return a list of reviews given the park name
async function fetchReviewsByPark(park_name){
   try {
      const response = await fetch(API + `reviews/parks/${park_name}`)
      if (!response){
         throw new Error("Could not fetch resource")
      }

      const data = await response.json()
      return data 
   }
   catch(error) {
      console.error(error)
   }
}


// Helper funciton to assist in display_page
function buildAddress(park){
   let addy = park.address;
   const new_addy = addy.line1 + " " + addy.city + ", " + addy.stateCode
   return new_addy
}


// Builds the full page dynamically 
async function display_page(park){
   page_title.textContent = park.park_name
   page_address.textContent = "Address: " + buildAddress(park)
   page_number.textContent = "Phone: " + park.contacts.phoneNumbers
   heading_background.style.background = `url(${park.images[0]}) no-repeat center center/cover`

   await display_reviews(park)
}



async function display_reviews(park){
   let reviews = await fetchReviewsByPark(park.park_name)
   review_container.innerHTML = "";

   reviews.forEach(review => {
      review_container.innerHTML += `
         <div>
            <h4>${review.park_name}</h4>
            <p><strong><i class="fa-regular fa-user"></i> User: </strong> ${review.user} </p>
            <p><strong><i class="fa-regular fa-star"></i> Rating: </strong>${review.rating}</p>
            <div class="review-description-container">
               <p><strong><i class="fa-regular fa-comment"></i> Description: </strong>${review.content} </p>
               
            </div>
            <button class="btn btn-outline-secondary" data-user = "${review.user}" data-review-id = "${review._id}">Edit</button>
            <button class="btn btn-danger" data-user = "${review.user}" data-review-id = "${review._id}">Delete</button>
            <hr>
         </div>
      `
   })
   

}





document.addEventListener('DOMContentLoaded', async function(){
   if (window.location.pathname.includes('reviews.html')){

      let park_name = localStorage.getItem("selectedParkName");
      let park_id = localStorage.getItem("selectedParkId");
   
      let park = await fetchParkByID(park_id)

      display_page(park)

      postReviewButton.addEventListener('click', async () =>{
         let rating = parseInt(document.getElementById("updateRating").value);
         let description = document.getElementById("postDescription").value;
         let rev_error = document.getElementById("review-error");

         if ((description.length >=5) && (rating>=1 && rating <=5)){
            await postReview("Temp", park.park_name, description, rating)

            // Clears modal input when post is successful
            document.getElementById("updateRating").value = ""
            document.getElementById("postDescription").value =""

            // Closes modal when post is successful
            const modalElement = document.getElementById('postModal');
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            modalInstance.hide();
            rev_error.style.display = "none"

            // Refresh reviews
            display_reviews(park)
         }
         else{
            
            rev_error.style.display = "block"
            
         }
      })

   }
})