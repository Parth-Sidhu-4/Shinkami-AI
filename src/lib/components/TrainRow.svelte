<script lang="ts">
	import type { Train } from '$lib/mockData';

	export let train: Train;
	export let onViewDetails: (train: Train) => void;

	// --- MODIFIED: The logic is updated to handle the new object structure ---
	let status: 'Ready' | 'On Hold' | 'Excluded';
	let statusColor: string;
	let reason: string;

	// Determine status and reason with a single, clear block of logic
	if (train.manual_override) {
		status = train.manual_override.decision === 'Induct' ? 'Ready' : 'Excluded';
		reason = `Override: ${train.manual_override.reason}`;
	} else if (train.violates_mandatory_fitness) {
		status = 'Excluded';
		reason = 'Fitness Expired';
	} else if (train.critical_job_card_flag) {
		status = 'Excluded';
		reason = 'Critical Job Card';
	} else if (train.cleaning_required && !train.cleaning_slot_booked) {
		status = 'On Hold';
		reason = 'Awaiting cleaning slot';
	} else {
		status = 'Ready';
		reason = 'All checks passed';
	}

	// Set color based on the final status
	if (status === 'Ready') {
		statusColor = 'bg-green-100 text-green-800';
	} else if (status === 'Excluded') {
		statusColor = 'bg-red-100 text-red-800';
	} else {
		// On Hold
		statusColor = 'bg-yellow-100 text-yellow-800';
	}
</script>

<tr class="border-b border-gray-200 hover:bg-gray-50">
	<td class="p-4">
		<span class="rounded-full px-3 py-1 text-sm font-semibold {statusColor}">
			{status}
		</span>
	</td>
	<td class="p-4 font-mono font-medium">{train.train_id}</td>
	<td class="p-4 text-gray-600">{reason}</td>
	<td class="p-4 text-center font-semibold">{train.readiness_probability}%</td>
	<td class="p-4 text-center">{train.odometer_total_km.toLocaleString()} km</td>
	<td class="p-4 text-center">{train.shunting_moves_needed}</td>
	<td class="p-4">
		<button on:click={() => onViewDetails(train)} class="text-blue-600 hover:underline">
			View Details
		</button>
	</td>
</tr>
