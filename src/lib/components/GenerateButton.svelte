<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
</script>

<button
	on:click={() => dispatch('click')}
	class="group relative inline-flex items-center justify-center overflow-hidden rounded-lg bg-gradient-to-tr from-blue-600 to-sky-500 px-6 py-3 font-bold text-white shadow-lg transition-all duration-300 ease-in-out hover:shadow-2xl"
>
	<span
		class="absolute bottom-0 left-0 mb-9 ml-9 h-48 w-48 -translate-x-full translate-y-full rotate-[-40deg] rounded-full bg-sky-400 opacity-40 transition-all duration-500 ease-out group-hover:translate-x-0"
	></span>
	<span class="relative">Generate Recommendation</span>
</button>
