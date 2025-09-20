<script lang="ts">
	import { auth } from '$lib/utils/firebase';
	import { signInWithEmailAndPassword } from 'firebase/auth';
	import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let errorMessage = '';
	let loading = false;

	async function login() {
		errorMessage = '';
		loading = true;
		try {
			await signInWithEmailAndPassword(auth, email, password);
			goto('/dashboard');
		} catch (error) {
			errorMessage = 'Unauthorized';
			console.error(error);
		} finally {
			loading = false;
		}
	}

	function closeLogin() {
		goto('/');
	}
</script>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-[#E0F7FA] to-[#F1F8E9] p-4"
>
	<div class="relative w-full max-w-md rounded-2xl bg-white p-8 shadow-2xl">
		<!-- Close button -->
		<button
			on:click={closeLogin}
			class="absolute top-4 right-4 flex h-10 w-10 items-center justify-center rounded-full bg-gray-200 text-gray-600 shadow-md transition hover:bg-gray-300 hover:text-gray-800 active:scale-95"
			aria-label="Close"
		>
			✕
		</button>

		<h1 class="mb-6 text-center text-3xl font-bold text-[#156B7D]">Welcome Back</h1>
		<p class="mb-6 text-center text-gray-500">Login to access your dashboard</p>

		<!-- Email input -->
		<div class="relative mb-4">
			<input
				type="email"
				placeholder="Email"
				bind:value={email}
				class="w-full rounded-lg border border-gray-300 px-4 py-3 pr-12 text-gray-700 placeholder-gray-400 transition outline-none focus:border-[#56A8A5] focus:ring-2 focus:ring-[#56A8A5]"
				disabled={loading}
			/>
			<span class="absolute top-1/2 right-3 -translate-y-1/2 text-lg text-gray-400">📧</span>
		</div>

		<!-- Password input -->
		<div class="relative mb-4">
			<input
				type="password"
				placeholder="Password"
				bind:value={password}
				class="w-full rounded-lg border border-gray-300 px-4 py-3 pr-12 text-gray-700 placeholder-gray-400 transition outline-none focus:border-[#56A8A5] focus:ring-2 focus:ring-[#56A8A5]"
				disabled={loading}
			/>
			<span class="absolute top-1/2 right-3 -translate-y-1/2 text-lg text-gray-400">🔒</span>
		</div>

		{#if errorMessage}
			<p class="mb-4 text-center text-sm text-red-500">{errorMessage}</p>
		{/if}

		<!-- Login button with spinner -->
		<button
			on:click={login}
			class="relative flex w-full items-center justify-center gap-2 rounded-lg bg-[#156B7D] py-3 font-semibold text-white shadow-lg transition hover:scale-105 hover:bg-[#0f4f5d]"
			disabled={loading}
		>
			{#if loading}
				<svg
					class="h-5 w-5 animate-spin text-white"
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
				>
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"
					></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
					></path>
				</svg>
				<span>Please wait...</span>
			{:else}
				Login
			{/if}
		</button>
	</div>
</div>
