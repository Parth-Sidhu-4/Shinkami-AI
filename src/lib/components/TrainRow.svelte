<script lang="ts">
	// Props
	export let train: Record<string, any>;
	export let onViewDetails: (train: Record<string, any>) => void;

	// Dynamically compute status color
	$: statusColor =
		train['Status'] === 'Ready'
			? 'bg-green-100 text-green-800'
			: train['Status'] === 'Excluded'
				? 'bg-red-100 text-red-800'
				: train['Status'] === 'On Hold'
					? 'bg-yellow-100 text-yellow-800'
					: 'bg-gray-200 text-gray-700';
</script>

<tr class="border-b border-gray-200 hover:bg-gray-50">
	<!-- Editable Status -->
	<td class="p-4">
		<select
			bind:value={train['Status']}
			class="rounded-full px-3 py-1 text-sm font-semibold {statusColor}"
		>
			<option value="Ready">Ready</option>
			<option value="Excluded">Excluded</option>
			<option value="On Hold">On Hold</option>
			<option value="Unknown">Unknown</option>
		</select>
	</td>

	<!-- Train ID (still editable? if yes, turn into input) -->
	<td class="p-4 font-mono font-medium">{train['Train ID']}</td>

	<!-- Editable fields -->
	<td class="p-4 text-gray-600">
		<input
			type="text"
			bind:value={train['Recommendation']}
			class="w-full rounded border px-2 py-1"
		/>
	</td>

	<td class="p-4 text-center font-semibold">
		<input
			type="number"
			bind:value={train['Readiness %']}
			class="w-20 rounded border px-2 py-1 text-center"
		/>
	</td>

	<td class="p-4 text-center">
		<input
			type="number"
			bind:value={train['Odometer']}
			class="w-24 rounded border px-2 py-1 text-center"
		/>
	</td>

	<td class="p-4 text-center">
		<input
			type="number"
			bind:value={train['Shunting Moves']}
			class="w-20 rounded border px-2 py-1 text-center"
		/>
	</td>

	<!-- Action -->
	<td class="p-4">
		<button on:click={() => onViewDetails(train)} class="text-blue-600 hover:underline">
			View Details
		</button>
	</td>
</tr>
