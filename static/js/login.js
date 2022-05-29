var firebaseConfig = {
    apiKey: "AIzaSyCcqMpVjuF0snEVmtC239IvQCbjt3vDTIM",
    authDomain: "xgensequencing.firebaseapp.com",
    projectId: "xgensequencing",
    storageBucket: "xgensequencing.appspot.com",
    messagingSenderId: "621187042000",
    appId: "1:621187042000:web:ab805ef860c1ae95082cd5",
    measurementId: "G-73YN3CVMT2"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);


function RegisterUser() {
    var email = document.getElementById('email_c').value;
    var password = document.getElementById('password_c').value;
    var name = document.getElementById('name_c').value;

    firebase.auth().createUserWithEmailAndPassword(email, password).then(function () {
        alert(name + ' Registered successfully');
        var id = firebase.auth().currentUser.uid;
        firebase.database().ref('/' + id).set({
            Name: name,
            Email: email,
        });
        // window.location.replace("login.html");
    }).catch(function (error) {

        var errorcode = error.code;
        var errormsg = error.message;
        alert('Error!!! Please Try Again...');

    });
}

function LoginUser() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    firebase.auth().signInWithEmailAndPassword(email, password).then(function () {

        var id = firebase.auth().currentUser.uid;
        window.location.replace("/");
        localStorage.setItem('id', id);

    }).catch(function (error) {
        alert("Incorrect Username or Password");
        var errorCode = error.code;
        var errorMsg = error.message;
    });
    // if (email == "abc@gmail.com" && password == "abhirup@123") {
    // 	window.location.replace("upload.html");
    // }
    // else {
    // 	alert("Incorrect Username or Password");
    // }
}

function LogoutUser() {
    firebase.auth().signOut().then(function () {
        // Sign-out successful.
        alert('User Logged Out!');
    }).catch(function (error) {
        // An error happened.
        console.log(error);
    });
}


const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});