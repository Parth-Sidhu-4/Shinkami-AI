<script lang="ts">
	import { createEventDispatcher, type EventDispatcher } from 'svelte';
	import type { Train } from '$lib/mockData';

	type ModalEvents = {
		close: null;
		induct: { reason: string };
		hold: { reason: string };
		preview: 'Induct' | 'Hold';
	};

	export let train: Train;
	const dispatch: EventDispatcher<ModalEvents> = createEventDispatcher();

	// --- NEW: State management for the two-step process ---
	let step: 'details' | 'reason_hold' | 'reason_induct' = 'details';

	const holdReasons = ['Awaiting Parts', 'Technician Unavailable', 'Safety Concern', 'Other'];
	const inductReasons = ['Priority Service', 'Branding Requirement', 'Testing Cycle', 'Other'];

	let selectedReasons: string[] = [];
	let otherReasonText = '';

	function closeModal() {
		// Reset state when closing
		step = 'details';
		selectedReasons = [];
		otherReasonText = '';
		dispatch('close');
	}

	function confirmOverride() {
		// 1. Compile the final reason from the user's selections
		let finalReason = selectedReasons.filter((r) => r !== 'Other').join(', ');
		if (selectedReasons.includes('Other') && otherReasonText) {
			if (finalReason) finalReason += '; ';
			finalReason += `Other: ${otherReasonText}`;
		}
		if (!finalReason) {
			finalReason = 'No reason provided.';
		}

		// 2. Dispatch the correct event based on which step we're in
		if (step === 'reason_hold') {
			dispatch('hold', { reason: finalReason });
		} else if (step === 'reason_induct') {
			dispatch('induct', { reason: finalReason });
		}

		// 3. Close the modal
		closeModal();
	}
</script>

<div
	on:click={closeModal}
	class="bg-opacity-60 fixed inset-0 z-40 flex items-center justify-center bg-black"
>
	<div on:click|stopPropagation class="z-50 w-full max-w-lg rounded-xl bg-white shadow-2xl">
		{#if step === 'details'}
			<div class="flex items-center justify-between border-b p-4">
				<h2 class="text-xl font-bold">Train Details: {train.train_id}</h2>
				<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800"
					>&times;</button
				>
			</div>

			<div class="grid grid-cols-2 gap-x-8 gap-y-4 p-6">
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Wear Index</h3>
					<p class="text-lg font-medium">{train.wear_index}</p>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Odometer</h3>
					<p class="text-lg font-medium">{train.odometer_total_km.toLocaleString()} km</p>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Critical Job Card?</h3>
					<p class:text-red-600={train.critical_job_card_flag} class="text-lg font-medium">
						{train.critical_job_card_flag ? 'Yes' : 'No'}
					</p>
				</div>
				<div>
					<h3 class="text-sm font-semibold text-gray-500">Fitness Valid?</h3>
					<p class:text-red-600={train.violates_mandatory_fitness} class="text-lg font-medium">
						{!train.violates_mandatory_fitness ? 'Yes' : 'No'}
					</p>
				</div>
				<div class="col-span-2">
					<h3 class="text-sm font-semibold text-gray-500">Score Breakdown</h3>
					<div class="mt-2 space-y-1 text-sm">
						<p>Readiness: <span class="font-bold">{train.score_components.readiness}</span></p>
						<p>Branding: <span class="font-bold">{train.score_components.branding}</span></p>
						<p>Shunting: <span class="font-bold">{train.score_components.shunting}</span></p>
					</div>
				</div>
			</div>

			<div class="border-t p-6">
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
			<div class="flex items-center justify-between border-b p-4">
				<h2 class="text-xl font-bold">Reason for Manual Override</h2>
				<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800"
					>&times;</button
				>
			</div>
			<div class="p-6">
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
