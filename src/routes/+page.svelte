<script lang="ts">
	import TrainRow from '$lib/components/TrainRow.svelte';
	import DetailsModal from '$lib/components/DetailsModal.svelte';
	import RecommendationModal from '$lib/components/RecommendationModal.svelte';
	import AuditLog from '$lib/components/AuditLog.svelte';
	import KpiSection from '$lib/components/KpiSection.svelte';
	import GenerateButton from '$lib/components/GenerateButton.svelte';
	import { mockTrains as initialTrains } from '$lib/mockData';
	import type { Train } from '$lib/mockData';
	import { slide } from 'svelte/transition';

	let showAuditLog = false;

	let mockTrains: Train[];
	let selectedTrain: Train | null = null;
	let recommendationResult: (Train & { rank_score: number })[] | null = null;
	let sortKey: keyof Train = 'train_id';
	let sortDirection: 'asc' | 'desc' = 'asc';
	let filterText = '';
	type LogEntry = { message: string; timestamp: Date };
	let logEntries: LogEntry[] = [];
	function getFakeAIPrediction(train: Train): number {
		if (train.violates_mandatory_fitness || train.critical_job_card_flag) return 0;
		if (train.cleaning_required && !train.cleaning_slot_booked) return 40;
		if (train.wear_index > 0.7) return 65;
		return 99;
	}
	function addToLog(message: string) {
		const newEntry: LogEntry = { message, timestamp: new Date() };
		logEntries = [newEntry, ...logEntries];
	}
	const processedTrains = initialTrains.map((train) => ({
		...train,
		readiness_probability: getFakeAIPrediction(train)
	}));
	mockTrains = processedTrains;
	function openModal(train: Train) {
		selectedTrain = train;
	}
	function closeModal() {
		selectedTrain = null;
	}
	const getStatus = (train: Train): 'Ready' | 'On Hold' | 'Excluded' => {
		if (train.manual_override?.decision === 'Induct') return 'Ready';
		if (train.manual_override?.decision === 'Hold') return 'Excluded';
		if (train.violates_mandatory_fitness || train.critical_job_card_flag) return 'Excluded';
		if (train.cleaning_required && !train.cleaning_slot_booked) return 'On Hold';
		return 'Ready';
	};
	function handleOverride(trainId: string, decision: 'Induct' | 'Hold', reason: string) {
		mockTrains = mockTrains.map((train) => {
			if (train.train_id === trainId) {
				const newOverride =
					train.manual_override?.decision === decision ? undefined : { decision, reason };
				return { ...train, manual_override: newOverride };
			}
			return train;
		});
		addToLog(`Supervisor forced ${decision.toUpperCase()} on train ${trainId}. Reason: ${reason}`);
	}
	function generateRecommendation() {
		const eligibleTrains = mockTrains.filter((t) => getStatus(t) === 'Ready');
		const scoredTrains = eligibleTrains.map((train) => {
			let score = 100;
			score -= train.wear_index * 10;
			score -= train.shunting_moves_needed * 2;
			if (train.branding_current_exposure_hours < train.branding_min_exposure_hours) {
				score += 5;
			}
			return { ...train, rank_score: score };
		});
		scoredTrains.sort((a, b) => b.rank_score - a.rank_score);
		recommendationResult = scoredTrains.slice(0, requiredServiceFleetSize);
		addToLog('System recommendation generated.');
	}
	function runPreview(trainId: string, decision: 'Induct' | 'Hold') {
		const simulatedTrains = mockTrains.map((t) => ({ ...t }));
		const trainToOverride = simulatedTrains.find((t) => t.train_id === trainId);
		if (trainToOverride) {
			trainToOverride.manual_override = { decision, reason: 'PREVIEW' };
		}
		const eligibleTrains = simulatedTrains.filter((t) => getStatus(t) === 'Ready');
		const scoredTrains = eligibleTrains.map((train) => {
			let score = 100;
			score -= train.wear_index * 10;
			score -= train.shunting_moves_needed * 2;
			if (train.branding_current_exposure_hours < train.branding_min_exposure_hours) {
				score += 5;
			}
			return { ...train, rank_score: score };
		});
		scoredTrains.sort((a, b) => b.rank_score - a.rank_score);
		recommendationResult = scoredTrains.slice(0, requiredServiceFleetSize);
		addToLog(`Previewed impact of ${decision.toUpperCase()} on train ${trainId}.`);
	}
	function sortBy(key: keyof Train) {
		if (sortKey === key) {
			sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDirection = 'asc';
		}
	}
	function exportToCsv() {
		addToLog('Data exported to CSV.');
		const headers = [
			'Train ID',
			'Status',
			'Reason',
			'Readiness %',
			'Mileage (km)',
			'Shunting Moves'
		];
		const rows = displayedTrains.map((train) => {
			const status = getStatus(train);
			const reason =
				train.manual_override?.reason ||
				(status === 'Ready'
					? 'All checks passed'
					: status === 'On Hold'
						? 'Awaiting cleaning slot'
						: 'System Excluded');
			return [
				train.train_id,
				status,
				`"${reason.replace(/"/g, '""')}"`,
				train.readiness_probability,
				train.odometer_total_km,
				train.shunting_moves_needed
			].join(',');
		});
		const csvContent = [headers.join(','), ...rows].join('\n');
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
		const link = document.createElement('a');
		const url = URL.createObjectURL(blob);
		link.setAttribute('href', url);
		link.setAttribute('download', `kmrl_roster_${new Date().toISOString().split('T')[0]}.csv`);
		link.style.visibility = 'hidden';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
	$: readyTrains = mockTrains.filter((t) => getStatus(t) === 'Ready');
	$: onHoldTrains = mockTrains.filter((t) => getStatus(t) === 'On Hold');
	$: excludedTrains = mockTrains.filter((t) => getStatus(t) === 'Excluded');
	$: totalShuntingMoves = readyTrains.reduce((sum, train) => sum + train.shunting_moves_needed, 0);
	const requiredServiceFleetSize = 20;
	$: displayedTrains = mockTrains
		.filter((train) => train.train_id.toLowerCase().includes(filterText.toLowerCase()))
		.sort((a, b) => {
			const valA = a[sortKey];
			const valB = b[sortKey];
			if (valA == null) return 1;
			if (valB == null) return -1;
			if (valA < valB) return sortDirection === 'asc' ? -1 : 1;
			if (valA > valB) return sortDirection === 'asc' ? 1 : -1;
			return 0;
		});
</script>

<div class="relative flex min-h-screen bg-slate-50 font-sans">
	<main class="flex-1 p-4 transition-all duration-300 md:p-8" class:lg:mr-96={showAuditLog}>
		<div class="mb-8">
			<div class="mb-4 flex items-center space-x-4">
				<div class="h-32 w-32 rounded-xl shadow-md">
					<img
						src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
						alt="Shinkami AI Logo"
						class="h-full w-full rounded-xl object-cover"
					/>
				</div>
				<p class="text-3xl font-bold text-slate-800">Welcome!</p>
			</div>
			<div class="flex items-center justify-between">
				<div>
					<h1 class="font-bold-italic text-4xl text-slate-800">KMRL Train Readiness</h1>
					<p class="mt-1 text-lg text-slate-500">Daily Operations Dashboard</p>
				</div>
				<GenerateButton on:click={generateRecommendation} />
			</div>
		</div>

		<KpiSection
			readyTrainsCount={readyTrains.length}
			onHoldTrainsCount={onHoldTrains.length}
			excludedTrainsCount={excludedTrains.length}
			{totalShuntingMoves}
			{requiredServiceFleetSize}
		/>

		<div class="mt-8">
			<div class="mb-4 flex items-center justify-between">
				<input
					type="text"
					bind:value={filterText}
					placeholder="Search by Train ID..."
					class="w-full max-w-xs rounded-lg border border-slate-300 p-2"
				/>
				<button
					on:click={exportToCsv}
					class="rounded-lg bg-slate-700 px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-slate-800"
				>
					Export to CSV
				</button>
			</div>
			<div class="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
				<table class="w-full text-left">
					<thead class="border-b border-gray-200 bg-gray-50">
						<tr class="text-sm text-gray-600 uppercase">
							<th class="p-4">Status</th>
							<th class="cursor-pointer p-4 hover:bg-gray-200" on:click={() => sortBy('train_id')}>
								Train ID {#if sortKey === 'train_id'}{sortDirection === 'asc' ? '▲' : '▼'}{/if}
							</th>
							<th class="p-4">Reason for Status</th>
							<th
								class="cursor-pointer p-4 text-center hover:bg-gray-200"
								on:click={() => sortBy('readiness_probability')}
							>
								Readiness % {#if sortKey === 'readiness_probability'}{sortDirection === 'asc'
										? '▲'
										: '▼'}{/if}
							</th>
							<th
								class="cursor-pointer p-4 text-center hover:bg-gray-200"
								on:click={() => sortBy('odometer_total_km')}
							>
								Mileage {#if sortKey === 'odometer_total_km'}{sortDirection === 'asc'
										? '▲'
										: '▼'}{/if}
							</th>
							<th
								class="cursor-pointer p-4 text-center hover:bg-gray-200"
								on:click={() => sortBy('shunting_moves_needed')}
							>
								Shunting Moves {#if sortKey === 'shunting_moves_needed'}{sortDirection === 'asc'
										? '▲'
										: '▼'}{/if}
							</th>
							<th class="p-4">Actions</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedTrains as train (train.train_id)}
							<TrainRow {train} onViewDetails={openModal} />
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</main>

	<aside
		class="fixed top-0 right-0 h-full w-96 transform bg-slate-800 text-white shadow-2xl transition-transform duration-300 ease-in-out"
		class:translate-x-0={showAuditLog}
		class:translate-x-full={!showAuditLog}
	>
		<div class="p-8">
			<AuditLog {logEntries} />
		</div>
	</aside>

	<button
		on:click={() => (showAuditLog = !showAuditLog)}
		class="fixed top-4 right-4 z-10 h-12 w-12 rounded-full bg-slate-800 text-white shadow-lg transition-all duration-300 ease-in-out hover:bg-slate-700"
		class:lg:right-[25rem]={showAuditLog}
		class:right-4={!showAuditLog}
		title="Toggle Audit Log"
	>
		{#if !showAuditLog}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="mx-auto h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 6h16M4 12h16M4 18h7"
				/></svg
			>
		{:else}
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="mx-auto h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M6 18L18 6M6 6l12 12"
				/></svg
			>
		{/if}
	</button>
</div>

{#if selectedTrain}
	<DetailsModal
		train={selectedTrain}
		on:close={closeModal}
		on:induct={(e) => handleOverride(selectedTrain!.train_id, 'Induct', e.detail.reason)}
		on:hold={(e) => handleOverride(selectedTrain!.train_id, 'Hold', e.detail.reason)}
		on:preview={(e) => runPreview(selectedTrain!.train_id, e.detail)}
	/>
{/if}

{#if recommendationResult}
	<RecommendationModal
		recommendedTrains={recommendationResult}
		on:close={() => (recommendationResult = null)}
	/>
{/if}
