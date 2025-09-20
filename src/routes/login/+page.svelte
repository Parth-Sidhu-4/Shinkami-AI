<script lang="ts">
	import { auth } from '$lib/utils/firebase';
	import { FirebaseError } from 'firebase/app';
	import { signInWithEmailAndPassword } from 'firebase/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let email = '';
	let password = '';
	let errorMessage = '';
	let loading = false;
	let emailInput: HTMLInputElement;

	// Autofocus the email input on page load for better UX
	onMount(() => {
		emailInput?.focus();
	});

	async function login() {
		if (!email || !password) {
			errorMessage = 'Please enter both email and password.';
			return;
		}
		errorMessage = '';
		loading = true;
		try {
			await signInWithEmailAndPassword(auth, email, password);
			goto('/dashboard');
		} catch (error) {
			// Provide more specific error messages based on the Firebase error code
			if (error instanceof FirebaseError) {
				switch (error.code) {
					case 'auth/user-not-found':
					case 'auth/invalid-email':
						errorMessage = 'No account found with that email address.';
						break;
					case 'auth/wrong-password':
						errorMessage = 'Incorrect password. Please try again.';
						break;
					default:
						errorMessage = 'An unexpected error occurred. Please try again.';
				}
			} else {
				errorMessage = 'Login failed. Please check your credentials.';
			}
			console.error(error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-slate-900 p-4">
	<div class="relative w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl">
		<a
			href="/"
			class="absolute top-4 right-4 flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-500 transition hover:bg-slate-200 hover:text-slate-800"
			aria-label="Close"
		>
			✕
		</a>

		<div class="mb-4 flex flex-col items-center text-center">
			<img
				src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
				alt="Shinkami AI Logo"
				class="h-16 w-16 rounded-lg"
			/>
			<h1 class="mt-4 text-2xl font-bold text-[#156B7D]">Welcome Back</h1>
			<p class="text-slate-500">Sign in to continue to your dashboard.</p>
		</div>

		<form on:submit|preventDefault={login} class="space-y-4">
			<div>
				<label for="email" class="mb-1 block text-sm font-medium text-slate-700"
					>Email Address</label
				>
				<div class="relative">
					<input
						bind:this={emailInput}
						bind:value={email}
						type="email"
						id="email"
						placeholder="you@example.com"
						class="w-full rounded-lg border-slate-300 px-4 py-2 pl-10 ring-offset-2 transition placeholder:text-slate-400 focus:ring-2 focus:ring-[#56A8A5]"
						disabled={loading}
						required
					/>
					<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 text-slate-400"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
							/></svg
						>
					</div>
				</div>
			</div>

			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-slate-700">Password</label>
				<div class="relative">
					<input
						bind:value={password}
						type="password"
						id="password"
						placeholder="••••••••"
						class="w-full rounded-lg border-slate-300 px-4 py-2 pl-10 ring-offset-2 transition placeholder:text-slate-400 focus:ring-2 focus:ring-[#56A8A5]"
						disabled={loading}
						required
					/>
					<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 text-slate-400"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							><path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
							/></svg
						>
					</div>
				</div>
			</div>

			{#if errorMessage}
				<p class="rounded-md bg-red-50 p-3 text-center text-sm font-medium text-red-600">
					{errorMessage}
				</p>
			{/if}

			<button
				type="submit"
				class="flex w-full items-center justify-center rounded-lg bg-[#156B7D] px-4 py-2.5 font-semibold text-white shadow-sm transition hover:bg-[#0f4f5d] disabled:cursor-not-allowed disabled:opacity-60"
				disabled={loading}
			>
				{#if loading}
					<svg class="mr-2 h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
						<circle
							class="opacity-25"
							cx="12"
							cy="12"
							r="10"
							stroke="currentColor"
							stroke-width="4"
						/>
						<path
							class="opacity-75"
							fill="currentColor"
							d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
						/>
					</svg>
					<span>Signing In...</span>
				{:else}
					Sign In
				{/if}
			</button>
		</form>
	</div>
</div>
