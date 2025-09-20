<script lang="ts">
	import { auth } from '$lib/utils/firebase';
	import { onAuthStateChanged } from 'firebase/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let checkingAuth = true; // show loading while checking auth

	onMount(() => {
		onAuthStateChanged(auth, (user) => {
			if (!user) {
				goto('/login'); // 🚨 redirect if not logged in
			}
			checkingAuth = false;
		});
	});
</script>

{#if checkingAuth}
	<div class="flex min-h-screen items-center justify-center">
		<p class="text-lg text-gray-500">Checking authentication...</p>
	</div>
{:else}
	<slot /> <!-- ✅ dashboard content will render here -->
{/if}
