// Run everything after page loads
document.addEventListener("DOMContentLoaded", function(){

// ================= FORM ELEMENTS =================
const form = document.getElementById('registrationForm');
const username = document.getElementById('username');
const email = document.getElementById('email');
const contact = document.getElementById('contact');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');
const successMessage = document.getElementById('successMessage');


// ================= PASSWORD TOGGLE =================
const togglePassword = document.getElementById('togglePassword');

if(togglePassword){
togglePassword.addEventListener('click', function () {

  const type = password.type === 'password' ? 'text' : 'password';
  password.type = type;

  this.classList.toggle('fa-eye');
  this.classList.toggle('fa-eye-slash');

});
}

const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');

if(toggleConfirmPassword){
toggleConfirmPassword.addEventListener('click', function () {

  const type = confirmPassword.type === 'password' ? 'text' : 'password';
  confirmPassword.type = type;

  this.classList.toggle('fa-eye');
  this.classList.toggle('fa-eye-slash');

});
}


// ================= CONTACT NUMBER ONLY =================
if(contact){
contact.addEventListener('input', function () {
  this.value = this.value.replace(/[^0-9]/g, '');
});
}


// ================= VALIDATION FUNCTIONS =================

function validateForm() {

let isValid = true;

// Username
if (username.value.trim() === '') {
showError('username','Username is required');
isValid = false;

} else if (username.value.trim().length < 3) {
showError('username','Username must be at least 3 characters');
isValid = false;

} else {
showSuccess('username');
}


// Email
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if (email.value.trim() === '') {
showError('email','Email is required');
isValid = false;

} else if (!emailRegex.test(email.value.trim())) {
showError('email','Enter valid email');
isValid = false;

} else {
showSuccess('email');
}


// Contact
const contactRegex = /^[6-9]\d{9}$/;

if (contact.value.trim() === '') {
showError('contact','Contact number required');
isValid = false;

} else if (!contactRegex.test(contact.value.trim())) {
showError('contact','Enter valid mobile number');
isValid = false;

} else {
showSuccess('contact');
}


// Password
if (password.value === '') {
showError('password','Password required');
isValid = false;

} else if (password.value.length < 6) {
showError('password','Minimum 6 characters');
isValid = false;

} else if (!hasUpperCase(password.value) || !hasNumber(password.value)) {
showError('password','Must contain uppercase & number');
isValid = false;

} else {
showSuccess('password');
}

return isValid;
}


// ================= HELPER FUNCTIONS =================

function hasUpperCase(str){
return /[A-Z]/.test(str);
}

function hasNumber(str){
return /\d/.test(str);
}


function showError(fieldName,message){

const input = document.getElementById(fieldName);
const errorDiv = document.getElementById(fieldName + 'Error');

if(input) input.classList.add('error');
if(input) input.classList.remove('success');

if(errorDiv){
errorDiv.textContent = message;
errorDiv.classList.add('show');
}

}


function showSuccess(fieldName){

const input = document.getElementById(fieldName);
const errorDiv = document.getElementById(fieldName + 'Error');

if(input) input.classList.add('success');
if(input) input.classList.remove('error');

if(errorDiv){
errorDiv.classList.remove('show');
}

}


function clearErrors(){

const inputs = document.querySelectorAll('.form-input');
const errors = document.querySelectorAll('.error-message');

inputs.forEach(input=>{
input.classList.remove('error','success');
});

errors.forEach(error=>{
error.classList.remove('show');
});

}


// ================= STATE → CITY =================

const stateSelect = document.getElementById("state");
const citySelect = document.getElementById("city");

if (stateSelect) {
  stateSelect.addEventListener("change", function() {
    const stateId = this.value;
    citySelect.innerHTML = '<option value="">Loading...</option>';
    citySelect.disabled = true;

    if (!stateId) {
      citySelect.innerHTML = '<option value="">Select State First</option>';
      citySelect.disabled = false;
      return;
    }

    fetch("/get-cities/" + stateId)
      .then(res => res.json())
      .then(data => {
        citySelect.innerHTML = '<option value="">Select City</option>';
        data.forEach(city => {
          let option = document.createElement("option");
          option.value = city.city_id;
          option.textContent = city.city_name;
          citySelect.appendChild(option);
        });
        citySelect.disabled = false;
      })
      .catch(err => {
        console.error("Error loading cities:", err);
        citySelect.innerHTML = '<option value="">Error loading cities</option>';
        citySelect.disabled = false;
      });
  });
}

});