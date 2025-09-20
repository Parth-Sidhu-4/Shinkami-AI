<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
</script>

<button
	on:click={() => dispatch('click')}
	class="group relative inline-flex items-center justify-center space-x-2 overflow-hidden rounded-xl bg-gradient-to-r from-[#56A8A5] to-[#82C24B] px-6 py-3 font-semibold text-white shadow-md transition-all duration-300 ease-out hover:scale-105 hover:shadow-xl"
>
	<!-- Glow effect -->
	<span
		class="absolute inset-0 h-full w-full bg-gradient-to-r from-white/20 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100"
	></span>

	<!-- Icon -->
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="2"
		stroke="currentColor"
		class="relative h-5 w-5"
	>
		<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
	</svg>

	<!-- Label -->
	<span class="relative">Generate Recommendation</span>
</button>
