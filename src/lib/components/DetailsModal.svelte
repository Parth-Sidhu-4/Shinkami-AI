<script lang="ts">
	import { createEventDispatcher, type EventDispatcher } from 'svelte';
	import { slide } from 'svelte/transition';

	type ModalEvents = {
		close: null;
		induct: { reason: string };
		hold: { reason: string };
		update: { updatedTrain: Record<string, any> };
	};

	export let train: Record<string, any>;
	const dispatch: EventDispatcher<ModalEvents> = createEventDispatcher();

	let step: 'details' | 'reason_hold' | 'reason_induct' = 'details';

	const holdReasons = ['Awaiting Parts', 'Technician Unavailable', 'Safety Concern', 'Other'];
	const inductReasons = ['Priority Service', 'Branding Requirement', 'Testing Cycle', 'Other'];

	let selectedReasons: string[] = [];
	let otherReasonText = '';

	function closeModal() {
		dispatch('update', { updatedTrain: train }); // Send back the updated train object
		dispatch('close');
		// Reset state after closing
		setTimeout(() => {
			step = 'details';
			selectedReasons = [];
			otherReasonText = '';
		}, 200); // Delay to allow fade-out
	}

	// --- Data processing for display ---
	const mainHeaders = [
		'Status',
		'Train ID',
		'Recommendation',
		'Readiness %',
		'Odometer',
		'Shunting Moves'
	];
	const excludedKeys = new Set(mainHeaders);

	const detailFieldLabels: Record<string, string> = {
		date: 'Date',
		depot: 'Depot',
		train_id: 'Train ID',
		rake_status_current: 'Rake Status Current',
		// ... (all your other labels remain the same)
		fitness_rolling_stock_expiry: 'Fitness Rolling Stock Expiry',
		fitness_signalling_expiry: 'Fitness Signalling Expiry',
		fitness_telecom_expiry: 'Fitness Telecom Expiry',
		fitness_all_valid: 'Fitness All Valid',
		open_job_cards_count: 'Open Job Cards Count',
		critical_job_card_flag: 'Critical Job Card Flag',
		job_card_last_update: 'Job Card Last Update',
		branding_contract_id: 'Branding Contract ID',
		branding_min_exposure_hours: 'Branding Min Exposure Hours',
		branding_current_exposure_hours_last_7d: 'Branding Exposure Hours (Last 7d)',
		branding_penalty_if_missed: 'Branding Penalty If Missed',
		odometer_total_km: 'Odometer Total KM',
		km_last_7d: 'KM Last 7d',
		km_last_30d: 'KM Last 30d',
		wear_index: 'Wear Index',
		cleaning_required: 'Cleaning Required',
		cleaning_slot_booked: 'Cleaning Slot Booked',
		cleaning_slot_time: 'Cleaning Slot Time',
		home_bay: 'Home Bay',
		bay_proximity_score: 'Bay Proximity Score',
		shunting_moves_needed: 'Shunting Moves Needed',
		crew_available_flag: 'Crew Available Flag',
		iot_temp_hvac_status: 'IoT Temp HVAC Status',
		telemetry_last_seen: 'Telemetry Last Seen',
		manual_override_flag: 'Manual Override Flag',
		whatsapp_update_count: 'WhatsApp Update Count',
		violates_mandatory_fitness: 'Violates Mandatory Fitness',
		violates_critical_job: 'Violates Critical Job',
		expected_shunting_energy_cost: 'Expected Shunting Energy Cost',
		rank_score: 'Rank Score',
		induction_decision: 'Induction Decision',
		unscheduled_withdrawal_within_24h: 'Unscheduled Withdrawal (24h)',
		probability_of_use: 'Probability of Use',
		recommendation: 'Recommendation',
		probability_rank: 'Probability Rank',
		final_score: 'Final Score'
	};

	$: detailEntries = Object.entries(train._original || train)
		.filter(([key]) => detailFieldLabels[key] && !excludedKeys.has(detailFieldLabels[key]))
		.map(([key, value]) => ({ key, label: detailFieldLabels[key], value }));
</script>

<div on:click={closeModal} class="fixed inset-0 z-40 flex items-center justify-center bg-black/60">
	<div
		on:click|stopPropagation
		class="z-50 flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-xl bg-white shadow-2xl"
	>
		{#if step === 'details'}
			<div in:slide={{ duration: 300 }}>
				<header class="flex items-center justify-between border-b p-4">
					<h2 class="text-xl font-bold">Train Details: {train['Train ID']}</h2>
					<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800"
						>&times;</button
					>
				</header>

				<div class="flex-1 overflow-y-auto p-6">
					<div class="grid grid-cols-1 gap-x-8 gap-y-4 md:grid-cols-2">
						{#each detailEntries as { key, label, value }}
							<div>
								<label for={key} class="text-sm font-semibold text-gray-500">{label}</label>
								<input
									id={key}
									type="text"
									value={train._original[key]}
									on:input={(e) => (train._original[key] = (e.target as HTMLInputElement).value)}
									class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:border-teal-500 focus:ring-teal-500"
								/>
							</div>
						{/each}
					</div>
				</div>

				<footer class="border-t bg-gray-50 p-4">
					<div class="rounded-lg border border-blue-200 bg-blue-50 p-4">
						<h3 class="font-bold text-blue-800">What-If Analysis & Manual Override</h3>
						<p class="mt-1 text-sm text-blue-700">
							Manually override the AI's recommendation. You will be asked to provide a reason.
						</p>
						<div class="mt-4 flex gap-4">
							<button
								on:click={() => (step = 'reason_induct')}
								class="flex-1 rounded-lg bg-green-600 px-4 py-2 font-bold text-white hover:bg-green-700"
								>Force Induct</button
							>
							<button
								on:click={() => (step = 'reason_hold')}
								class="flex-1 rounded-lg bg-red-600 px-4 py-2 font-bold text-white hover:bg-red-700"
								>Force Hold</button
							>
						</div>
					</div>
				</footer>
			</div>
		{/if}

		{#if step === 'reason_hold' || step === 'reason_induct'}
			<div in:slide={{ duration: 300 }}>
				<header class="border-b p-4">
					<h2 class="text-xl font-bold">
						{#if step === 'reason_hold'}Reason for Holding Train{/if}
						{#if step === 'reason_induct'}Reason for Inducting Train{/if}
					</h2>
					<p class="text-sm text-gray-500">Select all that apply.</p>
				</header>
			</div>
		{/if}
	</div>
</div>
