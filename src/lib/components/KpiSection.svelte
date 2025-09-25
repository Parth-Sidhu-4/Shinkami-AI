<script lang="ts">
	import KpiCard from '$lib/components/KpiCard.svelte';

	export let trains: any[]; // full CSV data
	export let requiredServiceFleetSize: number;
	export let riskStats: {
		maintenance: number;
		lowReadiness: number;
		holdInspection: number;
	};

	// ✅ Status-based counts
	$: readyTrainsCount = trains.filter((t) => t['Status'] === 'Ready').length;
	$: onHoldTrainsCount = trains.filter((t) => t['Status'] === 'On Hold').length;
	$: excludedTrainsCount = trains.filter((t) => t.Status === 'Excluded').length;
	$: totalShuntingMoves = trains.reduce((sum, t) => sum + (parseInt(t['Shunting Moves']) || 0), 0);
</script>

<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
	<KpiCard
		title="Trains for Service"
		value={`${readyTrainsCount} / ${requiredServiceFleetSize}`}
		subtitle="Ready vs. Required"
	>
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-green-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
			/>
		</svg>
	</KpiCard>

	<KpiCard title="⚠️ On Hold" value={onHoldTrainsCount.toString()} subtitle="Awaiting input">
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-yellow-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
			/>
		</svg>
	</KpiCard>

	<KpiCard title="❌ Excluded" value={excludedTrainsCount.toString()} subtitle="Critical blockers">
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-red-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
			/>
		</svg>
	</KpiCard>

	<KpiCard
		title="Shunting Moves"
		value={totalShuntingMoves.toString()}
		subtitle="For recommended lineup"
	>
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-blue-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M13 10V3L4 14h7v7l9-11h-7z"
			/>
		</svg>
	</KpiCard>
</div>

<!-- New Risk KPIs -->
<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
	<KpiCard
		title="🛠 Maintenance Due"
		value={riskStats.maintenance.toString()}
		subtitle="Needs scheduling"
	>
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-orange-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M9 17v-2h6v2m-7 4h8a2 2 0 002-2v-6a2 2 0 00-2-2h-1V7a4 4 0 10-8 0v4H8a2 2 0 00-2 2v6a2 2 0 002 2z"
			/>
		</svg>
	</KpiCard>

	<KpiCard title="📉 Low Readiness" value={riskStats.lowReadiness.toString()} subtitle="Below 60%">
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-purple-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
			/>
		</svg>
	</KpiCard>

	<KpiCard
		title="🔍 Hold for Inspection"
		value={riskStats.holdInspection.toString()}
		subtitle="Immediate action"
	>
		<svg
			slot="icon"
			xmlns="http://www.w3.org/2000/svg"
			class="h-8 w-8 text-pink-500"
			fill="none"
			viewBox="0 0 24 24"
			stroke="currentColor"
		>
			<path
				stroke-linecap="round"
				stroke-linejoin="round"
				stroke-width="2"
				d="M12 8c-1.104 0-2 .896-2 2s.896 2 2 2a2 2 0 100-4zm0 10c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z"
			/>
		</svg>
	</KpiCard>
</div>
