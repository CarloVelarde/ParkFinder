const API = "http://127.0.0.1:8000/";

let signUpForm = document.getElementById("signupForm");
let signInForm = document.getElementById("signinForm");

let signUpEmail = document.getElementById("signUpEmail");
let signUpPassword = document.getElementById("signUpPassword");

let signInEmail = document.getElementById("signInEmail");
let signInPassword = document.getElementById("signInPassword");

let success_fail_messageIN = document.getElementById("success_fail_messageIN")
let success_fail_messageUP = document.getElementById("success_fail_messageUP")



signUpForm.addEventListener('submit', function(event) {
   event.preventDefault();
   const email = signUpEmail.value;
   const password = signUpPassword.value;

   // Validate email with regex
   const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
   if (!emailRegex.test(email)) {
       console.error('Error: Invalid email format');

        //  Create Error messag
       success_fail_messageUP.textContent = "Please give a valid email.";
       success_fail_messageUP.style.color = "red";
       success_fail_messageUP.style.display = "inline";
       return;
   }

   // Validate password length
   if (password.length < 4) {
       console.error('Error: Password too short');
       //  Create Error message
       success_fail_messageUP.textContent = "Password must be at least 4 characters.";
       success_fail_messageUP.style.color = "red";
       success_fail_messageUP.style.display = "inline";
       return;
   }

   fetch(API + 'user/signup', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
       },
       body: JSON.stringify({ email, password })
   }).then(response => response.json())
     .then(data => {

         if (data.detail === "User with email provided exists already."){
            success_fail_messageUP.textContent = "Email already exists.";
            success_fail_messageUP.style.color = "red";
            success_fail_messageUP.style.display = "inline";
            throw new Error ("User with email provided exists already.")
         }
         console.log('Signup successful', data);

         //  Create Success message
         success_fail_messageUP.textContent = "Successfully signed up!";
         success_fail_messageUP.style.color = "green";
         success_fail_messageUP.style.display = "inline";

          //  Clear values
         signUpEmail.value = "";
         signUpPassword.value = "";


     }).catch(error => console.error('Error:', error));
});




signInForm.addEventListener('submit', function(event) {
   event.preventDefault();
   const email = signInEmail.value;
   const password = signInPassword.value;

   // Use URLSearchParams to construct the form data.
   const formData = new URLSearchParams();
   formData.append('username', email);
   formData.append('password', password);

   fetch(API + 'user/sign-in', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/x-www-form-urlencoded',
       },
       body: formData
   }).then(response => {
       if (response.ok) { // Checks if the response status code is 2xx
           return response.json(); // Parses the JSON body and passes the next promise
       } else {
           throw new Error('Failed to login'); // Throw an error to be caught later
       }
   }).then(data => {
       console.log('Login successful', data);
       localStorage.setItem('jwt', data.access_token); // Store the JWT token
       localStorage.setItem('userName', email)
       
      //  Create Success message
       success_fail_messageIN.textContent = "Successfully signed in!";
       success_fail_messageIN.style.color = "green";
       success_fail_messageIN.style.display = "inline";

      //  Clear values
      signInEmail.value = "";
      signInPassword.value = "";


       
   }).catch(error => {
       console.error('Error:', error);
       success_fail_messageIN.textContent = "Failed to login.";
       success_fail_messageIN.style.color = "red";
       success_fail_messageIN.style.display = "inline";
   });
});
