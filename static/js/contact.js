var config = {
  apiKey: "AIzaSyCcqMpVjuF0snEVmtC239IvQCbjt3vDTIM",
  authDomain: "xgensequencing.firebaseapp.com",
  projectId: "xgensequencing",
  storageBucket: "xgensequencing.appspot.com",
  databaseURL: "https://xgensequencing-default-rtdb.firebaseio.com/",
  messagingSenderId: "621187042000",
  appId: "1:621187042000:web:ab805ef860c1ae95082cd5",
  measurementId: "G-73YN3CVMT2"
};
firebase.initializeApp(config);

// Reference messages collection
var messagesRef = firebase.database().ref('messages');

// Listen for form submit
document.getElementById('contactForm').addEventListener('submit', submitForm);

// Submit form
function submitForm(e) {
  e.preventDefault();

  // Get values
  var name = getInputVal('name');
  var company = getInputVal('company');
  var email = getInputVal('email');
  var phone = getInputVal('phone');
  var message = getInputVal('message');

  // Save message
  saveMessage(name, company, email, phone, message);

  // Show alert
  document.querySelector('.alert').style.display = 'block';

  // Hide alert after 3 seconds
  setTimeout(function () {
    document.querySelector('.alert').style.display = 'none';
  }, 3000);

  // Clear form
  document.getElementById('contactForm').reset();
}

// Function to get get form values
function getInputVal(id) {
  return document.getElementById(id).value;
}

// Save message to firebase
function saveMessage(name, company, email, phone, message) {
  var newMessageRef = messagesRef.push();
  newMessageRef.set({
    name: name,
    company: company,
    email: email,
    phone: phone,
    message: message
  });
}