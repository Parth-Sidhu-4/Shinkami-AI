// src/lib/utils/firebase.ts
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
	apiKey: 'AIzaSyB5IklO2-Bwy2du-ECbdnkqgQavJZhhsNg',
	authDomain: 'shinkami-ai.firebaseapp.com',
	projectId: 'shinkami-ai',
	storageBucket: 'shinkami-ai.firebasestorage.app',
	messagingSenderId: '908551790242',
	appId: '1:908551790242:web:1496866afa34f5dfd241fb',
	measurementId: 'G-18PR5EQDJ7'
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
