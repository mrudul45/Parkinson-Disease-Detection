
let prediction = document.getElementById('prediction');
let probability = document.getElementById('probability');
let result = document.getElementById('result');
let title = document.getElementById('title');
let mainContainer = document.getElementById('main-container');
let refresh = document.getElementById('refresh');


refresh.style.display = 'none';


refresh.addEventListener('click',()=>{
    window.location.reload();
})

result.style.display = 'none';
// Get the form element by its ID or any other selector
var form = document.querySelector('form');
let loading = document.getElementById('loading');
loading.style.display = 'none';
function checkRadioButtons() {

var radioButtons = document.getElementsByName("model");
for (var i = 0; i < radioButtons.length; i++) {
var labelId = radioButtons[i].id + "-label"; 
var label = document.getElementById(labelId);

if (radioButtons[i].checked) {
    if (label) {
        label.style.backgroundColor = "#34eb86";
        label.style.color = "#fff"
    }
} else {
    if (label) {
        label.style.backgroundColor = "white";
        label.style.color = "#000"
    }
}
}
}

form.addEventListener('submit', function(event) {
// Prevent the default form submission behavior
event.preventDefault();
loading.style.display = 'flex';

// Set a timeout for submitting the form after 2 seconds (for example)
setTimeout(function() {
// Serialize the form data
var formData = new FormData(form);

// Make an HTTP POST request using fetch
fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if needed
    }
})
.then(response => {
    // Handle the response
    if (response.ok) {
        // If the response is successful (status code 200-299)
        return response.json(); // Assuming the response is JSON
    } else {
        // If the response is not successful, throw an error
        throw new Error('Failed to submit form');
    }
})
.then(data => {
    // Handle the data returned by the server
    console.log(data); 
    loading.style.display = 'none';
    mainContainer.style.display = 'none';
    refresh.style.display = 'initial';
    title.innerHTML = 'Result';
    result.style.display = 'initial';
    prediction.innerHTML = data['prediction'];
    if(data['prediction'] == "You have Parkinson's Disease."){
        probability.innerHTML = `You have ${data['prediction2']}% probability of having Parkinsons Disease..!`;
    } else {
        probability.innerHTML = `You have ${data['prediction2']}% probability of not having Parkinsons Disease..!`;
    }
})
.catch(error => {
    // Handle any errors that occurred during the fetch
    console.error('Error:', error);
});
}, 3000); // 2000 milliseconds (2 seconds) delay
});



// Function to get CSRF token from cookies
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
var cookies = document.cookie.split(';');
for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].trim();
    // Check if the cookie contains the CSRF token
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
    }
}
}
return cookieValue;
}