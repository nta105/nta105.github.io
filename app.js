// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDE18rHHX0vxRPKoMCPyATBIJuj7r5LkGE",
  authDomain: "website-2906b.firebaseapp.com",
  projectId: "website-2906b",
  storageBucket: "website-2906b.appspot.com",
  messagingSenderId: "1041544462060",
  appId: "1:1041544462060:web:457fb7ffd8e4abd6f6efc9",
  measurementId: "G-LQM3D2GC26"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    db.collection("messages").add({
        name: name,
        email: email,
        message: message
    })
    .then(() => {
        alert("Thank you! Your message has been sent.");
        document.getElementById('contactForm').reset(); // Correct the form ID for resetting
    })
    .catch((error) => {
        console.error("Error adding document: ", error);
        alert("Sorry, there was a problem sending your message.");
    });
});
