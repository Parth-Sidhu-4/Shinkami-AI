<script lang="ts">
	import Papa from 'papaparse';
	import DetailsModal from '$lib/components/DetailsModal.svelte';
	import RecommendationModal from '$lib/components/RecommendationModal.svelte';
	import AuditLog from '$lib/components/AuditLog.svelte';
	import KpiSection from '$lib/components/KpiSection.svelte';
	import GenerateButton from '$lib/components/GenerateButton.svelte';
	import FileUpload from '$lib/components/FileUpload.svelte';
	import { auth } from '$lib/utils/firebase';
	import { signOut } from 'firebase/auth';
	import { goto } from '$app/navigation';

	let showAuditLog = false;
	let currentTab: 'dashboard' | 'logs' | 'hints' = 'dashboard';
	let csvData: any[] = [];
	let selectedTrain: any = null;
	let recommendationResult: any[] | null = null;
	let filterText = '';
	let uploadedFile: File | null = null;
	type LogEntry = { message: string; timestamp: Date };
	let logEntries: LogEntry[] = [];
	let requiredServiceFleetSize = 0;
	$: requiredServiceFleetSize = csvData.length;
	let isEdited = false;
	let loadingRecommendation = false;

	export const columnMap: Record<string, string> = {
		train_id: 'Train ID',
		rake_status_current: 'Status',
		recommendation: 'Recommendation',
		probability_of_use: 'Readiness %',
		odometer_total_km: 'Odometer',
		shunting_moves_needed: 'Shunting Moves'
	};

	const mainHeaders = Object.values(columnMap);

	async function handleLogout() {
		await signOut(auth);
		goto('/');
	}

	function addToLog(message: string) {
		const newEntry: LogEntry = { message, timestamp: new Date() };
		logEntries = [newEntry, ...logEntries];
	}

	function exportEditedCsv(): string {
		const headers = mainHeaders;
		const rows = csvData.map((row) => {
			const obj: Record<string, any> = {};
			headers.forEach((h) => (obj[h] = row[h]));
			return obj;
		});
		return Papa.unparse(rows);
	}

	function handleCsvUpload() {
		if (!uploadedFile) return;
		Papa.parse(uploadedFile, {
			header: true,
			skipEmptyLines: true,
			complete: (results) => {
				if (!results.data || !Array.isArray(results.data)) {
					addToLog('CSV parse failed.');
					return;
				}
				csvData = (results.data as any[]).map((row: any) => {
					if (!row) return {};
					let status = '';
					switch ((row['rake_status_current'] || '').toLowerCase()) {
						case 'in_service':
							status = 'Ready';
							break;
						case 'in_ibl':
							status = 'On Hold';
							break;
						case 'stabled':
							status = 'Excluded';
							break;
						default:
							status = row['rake_status_current'] || '';
					}
					return {
						'Train ID': row['train_id'] ?? '',
						Odometer: row['odometer_total_km'] ?? '',
						Recommendation: row['recommendation'] ?? '',
						'Readiness %': row['probability_of_use'] ?? '',
						'Shunting Moves': row['shunting_moves_needed'] ?? '',
						Status: status,
						_original: row
					};
				});
				isEdited = false;
				addToLog(`CSV uploaded: ${uploadedFile.name}`);
			},
			error: (err) => {
				console.error(err);
				addToLog('Error parsing CSV.');
			}
		});
	}

	async function saveEditedData() {
		try {
			const csvString = exportEditedCsv();
			const blob = new Blob([csvString], { type: 'text/csv' });
			const formData = new FormData();
			formData.append('file', blob, 'edited.csv');
			const response = await fetch('/api/upload', {
				method: 'POST',
				body: formData
			});
			if (!response.ok) throw new Error('Upload failed');
			addToLog('Edited CSV uploaded successfully.');
			isEdited = false;
		} catch (err) {
			console.error(err);
			addToLog('Error uploading edited CSV.');
		}
	}

	function updateCell(rowIndex: number, key: string, value: string) {
		if (!csvData[rowIndex]) return;
		csvData[rowIndex][key] = value;
		isEdited = true;
	}

	async function generateRecommendation() {
		if (!uploadedFile && !isEdited) {
			addToLog('No CSV file uploaded for recommendation.');
			return;
		}
		try {
			loadingRecommendation = true;
			const formData = new FormData();
			if (isEdited) {
				const csvString = exportEditedCsv();
				const blob = new Blob([csvString], { type: 'text/csv' });
				formData.append('file', blob, 'edited.csv');
				addToLog('Using edited data for recommendations.');
			} else if (uploadedFile) {
				formData.append('file', uploadedFile);
				addToLog('Using original uploaded file.');
			}
			const response = await fetch('/api/predict', { method: 'POST', body: formData });
			if (!response.ok) {
				const errText = await response.text();
				throw new Error(`API Error: ${errText}`);
			}
			const respText = await response.text();
			const parsed = Papa.parse(respText, { header: true, skipEmptyLines: true });
			if (!parsed.data || !Array.isArray(parsed.data))
				throw new Error('Invalid CSV returned from API');
			csvData = parsed.data.map((row: any) => ({
				'Train ID': row['train_id'] ?? '',
				Odometer: row['odometer_total_km'] ?? '',
				Recommendation: row['recommendation'] ?? '',
				'Readiness %':
					row['predicted_probability_of_use'] !== undefined
						? (row['predicted_probability_of_use'] * 100).toFixed(1) + '%'
						: row['probability_of_use'] !== undefined
							? (row['probability_of_use'] * 100).toFixed(1) + '%'
							: '',
				'Shunting Moves': row['shunting_moves_needed'] ?? '',
				Status: row['rake_status_current'] ?? '',
				_original: row
			}));
			addToLog('New recommendations fetched from API.');
			isEdited = false;
		} catch (err) {
			console.error(err);
			addToLog('Error generating recommendations.');
		} finally {
			loadingRecommendation = false;
		}
	}

	function openModal(train: any) {
		selectedTrain = train;
	}
	function closeModal() {
		selectedTrain = null;
	}

	$: displayedTrains = csvData.filter((train) =>
		(train['Train ID'] || '').toString().toLowerCase().includes(filterText.toLowerCase())
	);
</script>

<nav
	class="sticky top-0 z-30 flex items-center justify-between bg-white/80 px-4 py-3 shadow-sm backdrop-blur-lg transition-all duration-300 md:px-8"
	class:lg:mr-96={showAuditLog}
>
	<a href="/" class="flex items-center space-x-3">
		<img
			src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
			alt="Shinkami AI Logo"
			class="h-12 w-12 rounded-lg"
		/>
		<span
			class="bg-gradient-to-r from-[#156B7D] via-[#56A8A5] to-[#82C24B] bg-clip-text text-2xl font-black tracking-tighter text-transparent"
			style="font-family: 'Montserrat', sans-serif;"
		>
			Shinkami AI
		</span>
	</a>

	<div class="flex items-center space-x-4">
		<a
			href="/"
			class="hidden rounded-lg px-3 py-2 font-medium text-slate-600 transition-colors duration-300 hover:text-[#156B7D] sm:block"
		>
			Home
		</a>

		<button
			on:click={handleLogout}
			class="rounded-lg px-4 py-2 text-sm font-semibold text-[#156B7D] ring-1 ring-[#156B7D] transition-colors duration-300 ring-inset hover:bg-[#156B7D] hover:text-white"
		>
			Logout
		</button>
	</div>
</nav>
<div class="relative flex min-h-screen bg-gray-50 text-[#333]">
	<main class="flex-1 p-6 md:p-10" class:lg:mr-96={showAuditLog}>
		<!-- Header -->
		<div
			class="mb-8 flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
		>
			<div class="flex items-center space-x-4">
				<div>
					<h1 class="text-3xl font-bold text-[#156B7D]">KMRL Train Readiness</h1>
					<p class="text-gray-600">Daily Operations Dashboard</p>
				</div>
			</div>
			<div class="flex items-center space-x-3">
				<GenerateButton on:click={generateRecommendation} disabled={loadingRecommendation} />

				<!-- Move Audit Log button here -->
				<button
					on:click={() => (showAuditLog = !showAuditLog)}
					class="rounded-full bg-[#156B7D] px-4 py-2 text-white shadow-lg transition hover:bg-[#0f4f5d] active:scale-95"
				>
					{#if !showAuditLog}☰{:else}✕{/if}
				</button>
			</div>
		</div>

		<!-- KPI Section -->
		{#if currentTab === 'dashboard'}
			<KpiSection trains={csvData} {requiredServiceFleetSize} />

			<!-- Controls -->
			<div class="mt-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
				<input
					type="text"
					bind:value={filterText}
					placeholder="Search by Train ID..."
					class="flex-1 rounded-lg border border-gray-300 p-2 shadow-sm focus:ring-2 focus:ring-[#56A8A5]"
				/>
				<div class="flex flex-wrap items-center gap-2">
					<FileUpload
						onUpload={(file) => {
							uploadedFile = file;
							handleCsvUpload();
						}}
					/>
					{#if uploadedFile}
						<span class="text-sm text-gray-500">{uploadedFile.name}</span>
					{/if}
					{#if isEdited}
						<button
							on:click={saveEditedData}
							class="rounded-lg bg-[#156B7D] px-4 py-2 text-sm font-semibold text-white shadow transition hover:bg-[#0f4f5d]"
						>
							Save & Upload
						</button>
					{/if}
				</div>
			</div>

			<!-- Train Table -->
			{#if csvData.length > 0}
				<div class="mt-6 overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-lg">
					<table class="w-full table-auto text-left">
						<thead class="sticky top-0 z-10 bg-[#56A8A5]/10 text-sm text-[#156B7D] uppercase">
							<tr>
								{#each mainHeaders as h}
									<th class="p-4">{h}</th>
								{/each}
								<th class="p-4">Actions</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200">
							{#each displayedTrains as row, i}
								<tr class="transition even:bg-gray-50 hover:bg-[#f0fdfa]">
									{#each mainHeaders as h}
										<td class="p-2">
											{#if h === 'Status'}
												<select
													class="w-full rounded-lg border-none px-2 py-1 text-sm font-semibold transition"
													class:bg-emerald-100={row[h] === 'Ready'}
													class:text-emerald-800={row[h] === 'Ready'}
													class:bg-amber-100={row[h] === 'On Hold'}
													class:text-amber-800={row[h] === 'On Hold'}
													class:bg-rose-100={row[h] === 'Excluded'}
													class:text-rose-800={row[h] === 'Excluded'}
													bind:value={row[h]}
													on:change={() => updateCell(i, h, row[h])}
												>
													<option value="Ready">Ready</option>
													<option value="On Hold">On Hold</option>
													<option value="Excluded">Excluded</option>
												</select>
											{:else if h === 'Recommendation'}
												<select
													class="w-full rounded border border-gray-300 bg-white p-1 text-sm text-[#333]"
													bind:value={row[h]}
													on:change={() => updateCell(i, h, row[h])}
												>
													<option value="Ready for service">Ready for service</option>
													<option value="Schedule maintenance soon"
														>Schedule maintenance soon</option
													>
													<option value="Hold for immediate inspection"
														>Hold for immediate inspection</option
													>
												</select>
											{:else if h === 'Odometer' || h === 'Shunting Moves'}
												<input
													class="w-full rounded border border-gray-300 bg-white p-1 text-sm"
													type="number"
													step={h === 'Odometer' ? '0.01' : '1'}
													bind:value={row[h]}
													on:input={() => updateCell(i, h, row[h])}
												/>
											{:else}
												<span class="px-2 py-1 text-sm">{row[h]}</span>
											{/if}
										</td>
									{/each}
									<td class="p-2">
										<button
											on:click={() => openModal(row)}
											class="font-semibold text-[#156B7D] hover:underline"
										>
											View Details
										</button>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if displayedTrains.length === 0}
						<p class="p-4 text-center text-gray-500">No trains found matching your search.</p>
					{/if}
				</div>
			{/if}
		{:else if currentTab === 'logs'}
			<div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
				<AuditLog {logEntries} />
			</div>
		{:else if currentTab === 'hints'}
			<div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
				<p class="text-gray-600">Hints will be displayed here.</p>
			</div>
		{/if}
	</main>

	<!-- Audit Log Sidebar -->
	<aside
		class="fixed top-0 right-0 z-10 h-full w-96 transform bg-white shadow-2xl transition-all duration-300 ease-in-out"
		class:translate-x-0={showAuditLog}
		class:translate-x-full={!showAuditLog}
	>
		<div class="space-y-4 p-6">
			<h2 class="text-lg font-bold text-[#156B7D]">Audit Log</h2>
			<AuditLog {logEntries} />
		</div>
	</aside>
</div>

<!-- Modals -->
{#if selectedTrain}
	<div
		class="fixed inset-0 z-40 flex items-center justify-center bg-black/60 p-4"
		on:click={closeModal}
	>
		<div
			class="flex h-full max-h-[90vh] w-full max-w-2xl flex-col rounded-lg bg-white shadow-xl"
			on:click|stopPropagation
		>
			<div class="flex items-center justify-between border-b p-4">
				<h3 class="text-xl font-bold text-slate-800">Edit Details: {selectedTrain['Train ID']}</h3>
				<button
					on:click={closeModal}
					class="rounded-full p-1 text-2xl leading-none text-slate-500 hover:bg-slate-100"
					>&times;</button
				>
			</div>

			<div class="flex-1 overflow-y-auto p-6">
				<div class="grid grid-cols-1 gap-x-6 gap-y-4 md:grid-cols-2">
					{#each Object.entries(selectedTrain._original) as [key, value]}
						<div>
							<label for={key} class="font-medium text-slate-500 capitalize"
								>{key.replace(/_/g, ' ')}</label
							>
							<input
								id={key}
								type="text"
								{value}
								on:input={(e) => {
									selectedTrain['_original'][key] = (e.target as HTMLInputElement).value;
									isEdited = true;
								}}
								class="mt-1 w-full rounded-md border-slate-300 p-2 font-semibold text-slate-900 shadow-sm focus:border-teal-500 focus:ring-teal-500"
							/>
						</div>
					{/each}
				</div>
			</div>

			<div class="border-t bg-slate-50 p-4 text-right">
				<button
					on:click={closeModal}
					class="rounded-md bg-slate-200 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-300"
					>Done</button
				>
			</div>
		</div>
	</div>
{/if}

{#if recommendationResult}
	<RecommendationModal
		recommendedTrains={recommendationResult}
		on:close={() => (recommendationResult = null)}
	/>
{/if}
