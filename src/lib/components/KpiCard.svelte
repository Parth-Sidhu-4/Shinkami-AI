<script lang="ts">
	export let title: string;
	export let value: string;
	export let subtitle: string = '';
</script>

<div class="flex items-center space-x-4 rounded-lg bg-white p-5 shadow-md">
	<div class="flex-shrink-0">
		<slot name="icon" />
	</div>
	<div class="flex-1">
		<p class="text-sm font-medium text-gray-500">{title}</p>
		<p class="mt-1 text-3xl font-bold text-gray-900">{value}</p>
		{#if subtitle}
			<p class="mt-1 text-xs text-gray-400">{subtitle}</p>
		{/if}
	</div>
</div>
