<script lang="ts">
	type LogEntry = { message: string; timestamp: Date };
	export let logEntries: LogEntry[];
</script>

<div class="rounded-lg bg-white shadow-md">
	<h2 class="border-b p-4 text-lg font-bold">📝 Audit Log</h2>
	<ul class="max-h-[60vh] overflow-y-auto text-sm text-gray-700">
		{#each logEntries as entry (entry.timestamp)}
			<li class="border-b p-4 hover:bg-gray-50">
				<p class="font-semibold">{entry.message}</p>
				<p class="mt-1 text-xs text-gray-500">{entry.timestamp.toLocaleTimeString()}</p>
			</li>
		{:else}
			<li class="p-4 text-gray-500">No actions have been logged yet.</li>
		{/each}
	</ul>
</div>
