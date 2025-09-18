<script lang="ts">
	/* --- your script block remains unchanged --- */
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
	let uploadedFile: File | null = null;
	type LogEntry = { message: string; timestamp: Date };
	let logEntries: LogEntry[] = [];

	let requiredServiceFleetSize = 0;
	$: requiredServiceFleetSize = csvData.length;

	export const columnMap: Record<string, string> = {
		train_id: 'Train ID',
		rake_status_current: 'Status',
		recommendation: 'Recommendation',
		probability_of_use: 'Readiness %',
		odometer_total_km: 'Odometer',
		shunting_moves_needed: 'Shunting Moves'
	};
	const mainHeaders = Object.values(columnMap);

	function addToLog(message: string) {
		const newEntry: LogEntry = { message, timestamp: new Date() };
		logEntries = [newEntry, ...logEntries];
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
				addToLog(`CSV uploaded: ${uploadedFile.name}`);
			},
			error: (err) => {
				console.error(err);
				addToLog('Error parsing CSV.');
			}
		});
	}

	function updateCell(rowIndex: number, key: string, value: string) {
		if (!csvData[rowIndex]) return;
		csvData[rowIndex][key] = value;
	}

	async function generateRecommendation() {
		if (!uploadedFile) {
			addToLog('No CSV file uploaded for recommendation.');
			return;
		}
		try {
			const formData = new FormData();
			formData.append('file', uploadedFile);

			const response = await fetch('/api/predict', { method: 'POST', body: formData });
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

<!-- Layout -->
<div class="relative flex min-h-screen bg-gray-50 text-gray-900">
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
					<p class="text-gray-500">Daily Operations Dashboard</p>
				</div>
			</div>
			<GenerateButton on:click={generateRecommendation} />
		</div>

		<!-- Tabs -->
		<div class="mb-6 flex space-x-4">
			<button
				on:click={() => (currentTab = 'dashboard')}
				class="rounded-lg px-4 py-2 text-sm font-medium transition-colors duration-200
					{currentTab === 'dashboard'
					? 'bg-indigo-600 text-white shadow'
					: 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-100'}"
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
					class="w-full max-w-xs rounded-lg border border-gray-300 bg-white p-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200"
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
				<div class="mt-6 overflow-x-auto rounded-xl border border-gray-200 bg-white shadow">
					<table class="w-full text-left">
						<thead
							class="border-b border-gray-200 bg-gray-50 text-xs font-semibold text-gray-600 uppercase"
						>
							<tr>
								{#each mainHeaders as h}
									<th class="p-3">{h}</th>
								{/each}
								<th class="p-3">Actions</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-100">
							{#each displayedTrains as row, i}
								<tr class="hover:bg-gray-50">
									{#each mainHeaders as h}
										<td class="p-2">
											<!-- Inputs look lighter, cleaner -->
											{#if h === 'Status'}
												<select
													class="w-full rounded border border-gray-300 bg-white p-1 text-sm"
													bind:value={row[h]}
													on:change={(e) => updateCell(i, h, (e.target as HTMLSelectElement).value)}
												>
													<option value="On Hold">On Hold</option>
													<option value="Ready">Ready</option>
													<option value="Excluded">Excluded</option>
												</select>
											{:else if h === 'Recommendation'}
												<select
													class="w-full rounded border border-gray-300 bg-white p-1 text-sm"
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
												<span class="text-gray-800">{row[h]}</span>
											{:else}
												<input
													class="w-full rounded border border-gray-300 bg-white p-1 text-sm"
													type="text"
													bind:value={row[h]}
													on:input={(e) => updateCell(i, h, (e.target as HTMLInputElement).value)}
												/>
											{/if}
										</td>
									{/each}
									<td class="p-2">
										<button
											on:click={() => openModal(row)}
											class="text-sm font-medium text-indigo-600 hover:underline"
										>
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
			<div class="rounded-xl border border-gray-200 bg-white p-4 shadow">
				<AuditLog {logEntries} />
			</div>
		{:else if currentTab === 'hints'}
			<div class="rounded-xl border border-gray-200 bg-white p-4 shadow">
				<p class="text-gray-600">Hints will be displayed here.</p>
			</div>
		{/if}
	</main>

	<!-- Audit Log Sidebar -->
	<aside
		class="fixed top-0 right-0 h-full w-96 transform bg-white text-gray-900 shadow-2xl transition-transform duration-300 ease-in-out"
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
		class="fixed top-4 right-4 z-10 h-12 w-12 rounded-full bg-indigo-600 text-white shadow hover:bg-indigo-500"
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
