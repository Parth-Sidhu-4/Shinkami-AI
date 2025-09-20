import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import { writable } from 'svelte/store';
import { getAuth, onAuthStateChanged, signOut, type User } from 'firebase/auth';
import { app } from '$lib/utils/firebase'; // your firebase init file

export const auth = getAuth(app);
export const user = writable<User | null>(null);
export const authLoading = writable(true);

if (browser) {
	onAuthStateChanged(auth, (u) => {
		user.set(u);
		authLoading.set(false);
	});
}

export async function logout() {
	await signOut(auth);
	goto('/'); // back to homepage
}
