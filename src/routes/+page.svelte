<script lang="ts">
	import Papa from 'papaparse';
	import DetailsModal from '$lib/components/DetailsModal.svelte';
	import RecommendationModal from '$lib/components/RecommendationModal.svelte';
	import AuditLog from '$lib/components/AuditLog.svelte';
	import KpiSection from '$lib/components/KpiSection.svelte';
	import GenerateButton from '$lib/components/GenerateButton.svelte';
	import FileUpload from '$lib/components/FileUpload.svelte';

	let showAuditLog = false;
	let currentTab: 'dashboard' | 'logs' | 'hints' = 'dashboard';

	let csvData: any[] = [];
	let selectedTrain: any = null;
	let recommendationResult: any[] | null = null;
	let filterText = '';
	let uploadedFile: File | null = null; // ✅ store uploaded file
	type LogEntry = { message: string; timestamp: Date };
	let logEntries: LogEntry[] = [];

	let requiredServiceFleetSize = 0;
	$: requiredServiceFleetSize = csvData.length;

	// Backend → UI mapping
	export const columnMap: Record<string, string> = {
		train_id: 'Train ID',
		rake_status_current: 'Status',
		recommendation: 'Recommendation',
		probability_of_use: 'Readiness %',
		odometer_total_km: 'Odometer',
		shunting_moves_needed: 'Shunting Moves'
	};

	// Column order in table
	const mainHeaders = Object.values(columnMap);

	function addToLog(message: string) {
		const newEntry: LogEntry = { message, timestamp: new Date() };
		logEntries = [newEntry, ...logEntries];
	}

	// --- Upload CSV from user ---
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

				addToLog(`CSV uploaded: ${uploadedFile.name}`);
			},
			error: (err) => {
				console.error(err);
				addToLog('Error parsing CSV.');
			}
		});
	}

	// --- Inline editing ---
	function updateCell(rowIndex: number, key: string, value: string) {
		if (!csvData[rowIndex]) return;
		csvData[rowIndex][key] = value;
	}

	// --- Generate Recommendations from API ---
	async function generateRecommendation() {
		if (!uploadedFile) {
			addToLog('No CSV file uploaded for recommendation.');
			return;
		}

		try {
			const formData = new FormData();
			formData.append('file', uploadedFile);

			const response = await fetch('/api/predict', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				const errText = await response.text();
				throw new Error(`API Error: ${errText}`);
			}

			const respText = await response.text();
			const parsed = Papa.parse(respText, { header: true, skipEmptyLines: true });

			if (!parsed.data || !Array.isArray(parsed.data)) {
				throw new Error('Invalid CSV returned from API');
			}

			csvData = parsed.data.map((row: any) => {
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
					'Readiness %':
						row['predicted_probability_of_use'] !== undefined
							? (row['predicted_probability_of_use'] * 100).toFixed(1) + '%'
							: row['probability_of_use'] !== undefined
								? (row['probability_of_use'] * 100).toFixed(1) + '%'
								: '',
					'Shunting Moves': row['shunting_moves_needed'] ?? '',
					Status: status,
					_original: row
				};
			});

			addToLog('New recommendations fetched from API.');
		} catch (err) {
			console.error(err);
			addToLog('Error generating recommendations.');
		}
	}

	// --- Modal control ---
	function openModal(train: any) {
		selectedTrain = train;
	}
	function closeModal() {
		selectedTrain = null;
	}

	// --- Derived values ---
	$: displayedTrains = csvData.filter((train) =>
		(train['Train ID'] || '').toString().toLowerCase().includes(filterText.toLowerCase())
	);
</script>

<!-- Layout -->
<div
	class="relative flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-black text-white"
>
	<main class="flex-1 p-6 md:p-10" class:lg:mr-96={showAuditLog}>
		<!-- Header -->
		<div class="mb-8 flex items-center justify-between">
			<div class="flex items-center space-x-4">
				<img
					src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
					alt="Shinkami AI Logo"
					class="h-20 w-20 rounded-xl object-cover shadow-md"
				/>
				<div>
					<h1 class="text-3xl font-bold">KMRL Train Readiness</h1>
					<p class="text-slate-400">Daily Operations Dashboard</p>
				</div>
			</div>
			<GenerateButton on:click={generateRecommendation} />
		</div>

		<!-- Tabs -->
		<div class="mb-6 flex space-x-4">
			<button
				on:click={() => (currentTab = 'dashboard')}
				class="rounded-xl px-4 py-2 transition-all duration-200 {currentTab === 'dashboard'
					? 'bg-purple-600'
					: 'bg-purple-800/40'}"
			>
				Dashboard
			</button>
		</div>

		<!-- Panels -->
		{#if currentTab === 'dashboard'}
			<KpiSection trains={csvData} {requiredServiceFleetSize} />

			<!-- Controls -->
			<div class="mt-8 flex items-center justify-between space-x-4">
				<input
					type="text"
					bind:value={filterText}
					placeholder="Search by Train ID..."
					class="w-full max-w-xs rounded-lg border border-slate-300/20 bg-black/30 p-2 text-white"
				/>

				<div class="flex items-center space-x-2">
					<FileUpload
						onUpload={(file) => {
							uploadedFile = file;
							handleCsvUpload();
						}}
					/>
				</div>
			</div>

			<!-- Train Table -->
			{#if csvData.length > 0}
				<div
					class="mt-6 overflow-x-auto rounded-xl border border-slate-200/20 bg-white/5 shadow-sm"
				>
					<table class="w-full text-left">
						<thead class="border-b border-slate-200/10 bg-white/10">
							<tr class="text-sm text-slate-300 uppercase">
								{#each mainHeaders as h}
									<th class="p-4">{h}</th>
								{/each}
								<th class="p-4">Actions</th>
							</tr>
						</thead>
						<tbody>
							{#each displayedTrains as row, i}
								<tr>
									{#each mainHeaders as h}
										<td class="border border-slate-700 p-2">
											{#if h === 'Status'}
												<select
													class="w-full rounded border-none bg-slate-800 text-white"
													bind:value={row[h]}
													on:change={(e) => updateCell(i, h, (e.target as HTMLSelectElement).value)}
												>
													<option value="On Hold">On Hold</option>
													<option value="Ready">Ready</option>
													<option value="Excluded">Excluded</option>
												</select>
											{:else if h === 'Recommendation'}
												<select
													class="w-full rounded border-none bg-slate-800 text-white"
													bind:value={row[h]}
													on:change={(e) => updateCell(i, h, (e.target as HTMLSelectElement).value)}
												>
													<option value="Ready for service">Ready for service</option>
													<option value="Schedule maintenance soon"
														>Schedule maintenance soon</option
													>
													<option value="Hold for immediate inspection"
														>Hold for immediate inspection</option
													>
												</select>
											{:else if h === 'Readiness %'}
												<span>{row[h]}</span>
											{:else if h === 'Odometer'}
												<input
													class="w-full border-none bg-transparent"
													type="number"
													step="0.01"
													bind:value={row[h]}
													on:input={(e) =>
														updateCell(
															i,
															h,
															parseFloat((e.target as HTMLInputElement).value).toString()
														)}
												/>
											{:else if h === 'Shunting Moves'}
												<input
													class="w-full border-none bg-transparent"
													type="number"
													step="1"
													bind:value={row[h]}
													on:input={(e) =>
														updateCell(
															i,
															h,
															parseInt((e.target as HTMLInputElement).value).toString()
														)}
												/>
											{:else}
												<input
													class="w-full border-none bg-transparent"
													type="text"
													bind:value={row[h]}
													on:input={(e) => updateCell(i, h, (e.target as HTMLInputElement).value)}
												/>
											{/if}
										</td>
									{/each}
									<td class="p-2">
										<button on:click={() => openModal(row)} class="text-blue-400 hover:underline">
											View Details
										</button>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		{:else if currentTab === 'logs'}
			<div class="rounded-xl border border-white/10 bg-black/30 p-4">
				<AuditLog {logEntries} />
			</div>
		{:else if currentTab === 'hints'}
			<div class="rounded-xl border border-white/10 bg-black/30 p-4">
				<p class="text-slate-300">Hints will be displayed here.</p>
			</div>
		{/if}
	</main>

	<!-- Audit Log Sidebar -->
	<aside
		class="fixed top-0 right-0 h-full w-96 transform bg-slate-900 text-white shadow-2xl transition-transform duration-300 ease-in-out"
		class:translate-x-0={showAuditLog}
		class:translate-x-full={!showAuditLog}
	>
		<div class="p-8">
			<AuditLog {logEntries} />
		</div>
	</aside>

	<!-- Toggle Audit Log Button -->
	<button
		on:click={() => (showAuditLog = !showAuditLog)}
		class="fixed top-4 right-4 z-10 h-12 w-12 rounded-full bg-purple-700 hover:bg-purple-600"
		class:lg:right-[25rem]={showAuditLog}
		class:right-4={!showAuditLog}
	>
		{#if !showAuditLog}
			☰
		{:else}
			✕
		{/if}
	</button>
</div>

<!-- Modals -->
{#if selectedTrain}
	<DetailsModal train={selectedTrain} on:close={closeModal} />
{/if}

{#if recommendationResult}
	<RecommendationModal
		recommendedTrains={recommendationResult}
		on:close={() => (recommendationResult = null)}
	/>
{/if}
