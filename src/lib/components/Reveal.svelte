<script lang="ts">
	import { onMount } from 'svelte';

	let el: HTMLElement;
	let visible = false;

	onMount(() => {
		const observer = new IntersectionObserver(([entry]) => {
			if (entry.isIntersecting) {
				visible = true;
				observer.disconnect();
			}
		});
		if (el) observer.observe(el);
	});
</script>

<div bind:this={el} class:visible>
	<slot />
</div>

<style>
	div {
		opacity: 0;
		transform: translateY(20px);
		transition: all 0.6s ease;
	}
	div.visible {
		opacity: 1;
		transform: translateY(0);
	}
</style>
