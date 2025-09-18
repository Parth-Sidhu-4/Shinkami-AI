<script lang="ts">
	// A row parsed from CSV (plain object)
	export let train: Record<string, any>;
	export let onViewDetails: (train: Record<string, any>) => void;

	// Expect these columns from CSV
	let status: string = train['Status'] || 'Unknown';
	let trainId: string = train['Train ID'] || '';
	let recommendation: string = train['Recommendation'] || '';
	let readiness: string = train['Readiness %'] || '';
	let odometer: string = train['Odometer'] || '';
	let shunting: string = train['Shunting Moves'] || '';

	let statusColor: string;

	if (status === 'Ready') {
		statusColor = 'bg-green-100 text-green-800';
	} else if (status === 'Excluded') {
		statusColor = 'bg-red-100 text-red-800';
	} else if (status === 'On Hold') {
		statusColor = 'bg-yellow-100 text-yellow-800';
	} else {
		statusColor = 'bg-gray-200 text-gray-700';
	}
</script>

<tr class="border-b border-gray-200 hover:bg-gray-50">
	<td class="p-4">
		<span class="rounded-full px-3 py-1 text-sm font-semibold {statusColor}">
			{status}
		</span>
	</td>

	<td class="p-4 font-mono font-medium">{trainId}</td>
	<td class="p-4 text-gray-600">{recommendation}</td>
	<td class="p-4 text-center font-semibold">{readiness}</td>
	<td class="p-4 text-center">{odometer}</td>
	<td class="p-4 text-center">{shunting}</td>

	<td class="p-4">
		<button on:click={() => onViewDetails(train)} class="text-blue-600 hover:underline">
			View Details
		</button>
	</td>
</tr>
