<script lang="ts">
	import { createEventDispatcher, type EventDispatcher } from 'svelte';

	type ModalEvents = {
		close: null;
		induct: { reason: string };
		hold: { reason: string };
		preview: 'Induct' | 'Hold';
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
		step = 'details';
		selectedReasons = [];
		otherReasonText = '';
		dispatch('update', { updatedTrain: train }); // send updated values
		dispatch('close');
	}

	function confirmOverride() {
		let finalReason = selectedReasons.filter((r) => r !== 'Other').join(', ');
		if (selectedReasons.includes('Other') && otherReasonText) {
			if (finalReason) finalReason += '; ';
			finalReason += `Other: ${otherReasonText}`;
		}
		if (!finalReason) finalReason = 'No reason provided.';

		if (step === 'reason_hold') {
			dispatch('hold', { reason: finalReason });
		} else if (step === 'reason_induct') {
			dispatch('induct', { reason: finalReason });
		}
		closeModal();
	}

	// Fields shown in main table
	const mainHeaders = [
		'Status',
		'Train ID',
		'Recommendation',
		'Readiness %',
		'Odometer',
		'Shunting Moves'
	];
	const excludedKeys = new Set(mainHeaders);

	// Map CSV keys → UI labels
	const detailFieldLabels: Record<string, string> = {
		date: 'Date',
		depot: 'Depot',
		train_id: 'Train ID',
		rake_status_current: 'Rake Status Current',
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

	// Build detail entries from the original CSV row
	$: detailEntries = Object.entries(train._original || train)
		.filter(([key]) => detailFieldLabels[key] && !excludedKeys.has(detailFieldLabels[key]))
		.map(([key, value]) => [key, detailFieldLabels[key], value]);
</script>

<div
	on:click={closeModal}
	class="bg-opacity-60 fixed inset-0 z-40 flex items-center justify-center bg-black"
>
	<div
		on:click|stopPropagation
		class="z-50 flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-xl bg-white shadow-2xl"
	>
		{#if step === 'details'}
			<!-- Header -->
			<div class="flex items-center justify-between border-b p-4">
				<h2 class="text-xl font-bold">Train Details: {train['Train ID']}</h2>
				<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800">
					&times;
				</button>
			</div>

			<!-- Scrollable content -->
			<div class="flex-1 overflow-y-auto p-6">
				<div class="grid grid-cols-2 gap-x-8 gap-y-4">
					{#each detailEntries as [key, label, value]}
						<div class="col-span-2">
							<h3 class="text-sm font-semibold text-gray-500">{label}</h3>
							<input
								type="text"
								bind:value={train._original[key]}
								class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
							/>
						</div>
					{/each}
				</div>

				<!-- What-If Analysis -->
				<div class="mt-6 border-t pt-6">
					<h3 class="mb-3 text-sm font-semibold text-gray-500">What-If Analysis</h3>
					<p class="mb-3 text-xs text-gray-500">
						See how a manual override would impact the system's recommended lineup before committing
						to the change.
					</p>
					<div class="flex space-x-4">
						<button
							on:click={() => dispatch('preview', 'Induct')}
							class="w-full rounded-lg bg-gray-200 px-4 py-2 font-bold text-gray-800 hover:bg-gray-300"
						>
							Preview "Induct" Impact
						</button>
						<button
							on:click={() => dispatch('preview', 'Hold')}
							class="w-full rounded-lg bg-gray-200 px-4 py-2 font-bold text-gray-800 hover:bg-gray-300"
						>
							Preview "Hold" Impact
						</button>
					</div>
				</div>
			</div>

			<!-- Footer -->
			<div class="flex justify-end space-x-4 rounded-b-xl border-t bg-gray-50 p-4">
				<button
					on:click={() => (step = 'reason_hold')}
					class="rounded-lg bg-red-100 px-4 py-2 font-bold text-red-700 hover:bg-red-200"
				>
					Force Hold
				</button>
				<button
					on:click={() => (step = 'reason_induct')}
					class="rounded-lg bg-green-100 px-4 py-2 font-bold text-green-700 hover:bg-green-200"
				>
					Force Induct
				</button>
			</div>
		{:else}
			<!-- Override reasons -->
			<div class="flex items-center justify-between border-b p-4">
				<h2 class="text-xl font-bold">Reason for Manual Override</h2>
				<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800">
					&times;
				</button>
			</div>

			<div class="flex-1 overflow-y-auto p-6">
				<p class="mb-4 text-gray-600">
					Please select a reason for forcing this train to
					<strong>{step === 'reason_hold' ? 'Hold' : 'Induct'}</strong>.
				</p>

				<div class="space-y-3">
					{#if step === 'reason_hold'}
						{#each holdReasons as reason}
							<label class="flex items-center">
								<input
									type="checkbox"
									bind:group={selectedReasons}
									value={reason}
									class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
								/>
								<span class="ml-3 text-gray-700">{reason}</span>
							</label>
						{/each}
					{:else}
						{#each inductReasons as reason}
							<label class="flex items-center">
								<input
									type="checkbox"
									bind:group={selectedReasons}
									value={reason}
									class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
								/>
								<span class="ml-3 text-gray-700">{reason}</span>
							</label>
						{/each}
					{/if}
				</div>

				{#if selectedReasons.includes('Other')}
					<div class="mt-4">
						<input
							type="text"
							bind:value={otherReasonText}
							placeholder="Please specify other reason..."
							class="mt-1 w-full rounded-md border border-gray-300 p-2"
						/>
					</div>
				{/if}
			</div>

			<div class="flex items-center justify-between rounded-b-xl border-t bg-gray-50 p-4">
				<button
					on:click={() => (step = 'details')}
					class="rounded-lg px-4 py-2 font-bold text-gray-600 hover:bg-gray-200"
				>
					Back
				</button>
				<button
					on:click={confirmOverride}
					class="rounded-lg bg-blue-600 px-4 py-2 font-bold text-white hover:bg-blue-700"
				>
					Confirm Override
				</button>
			</div>
		{/if}
	</div>
</div>
