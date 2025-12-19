import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDPr-wG-tejan1BkiQ5cacgx8LrDT0YIZw",
  authDomain: "polistock-db.firebaseapp.com",
  projectId: "polistock-db",
  storageBucket: "polistock-db.firebasestorage.app",
  messagingSenderId: "581085910",
  appId: "1:581085910:web:d64444fcfb8d93b3a4f777",
  measurementId: "G-YNL3G59K6X",
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
