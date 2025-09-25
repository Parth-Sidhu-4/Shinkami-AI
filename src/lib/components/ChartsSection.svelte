<script lang="ts">
	import {
		PieChart,
		Pie,
		Cell,
		Tooltip,
		ResponsiveContainer,
		BarChart,
		CartesianGrid,
		XAxis,
		YAxis,
		Bar
	} from 'recharts';

	export let trains: any[] = [];

	// --- Readiness buckets ---
	$: readinessBuckets = [
		{
			name: '<60%',
			value: trains.filter((t) => parseFloat((t['Readiness %'] || '').replace('%', '')) < 60).length
		},
		{
			name: '60–80%',
			value: trains.filter((t) => {
				const val = parseFloat((t['Readiness %'] || '').replace('%', ''));
				return val >= 60 && val < 80;
			}).length
		},
		{
			name: '>80%',
			value: trains.filter((t) => parseFloat((t['Readiness %'] || '').replace('%', '')) >= 80)
				.length
		}
	];

	// --- Recommendation distribution ---
	$: recommendationCounts = [
		{
			name: 'Ready for service',
			value: trains.filter((t) => t.Recommendation === 'Ready for service').length
		},
		{
			name: 'Maintenance soon',
			value: trains.filter((t) => t.Recommendation === 'Schedule maintenance soon').length
		},
		{
			name: 'Immediate inspection',
			value: trains.filter((t) => t.Recommendation === 'Hold for immediate inspection').length
		}
	];

	// --- Status counts ---
	$: statusCounts = [
		{ name: 'Ready', value: trains.filter((t) => t.Status === 'Ready').length },
		{ name: 'On Hold', value: trains.filter((t) => t.Status === 'On Hold').length },
		{ name: 'Excluded', value: trains.filter((t) => t.Status === 'Excluded').length }
	];

	const COLORS = ['#82C24B', '#56A8A5', '#E74C3C', '#F39C12'];
</script>

<div class="mt-10 grid grid-cols-1 gap-6 lg:grid-cols-3">
	<!-- Readiness Distribution -->
	<div class="rounded-xl bg-white p-4 shadow">
		<h3 class="mb-2 text-lg font-semibold text-slate-700">Readiness Distribution</h3>
		<ResponsiveContainer width="100%" height={250}>
			<PieChart>
				<Pie dataKey="value" data={readinessBuckets} cx="50%" cy="50%" outerRadius={80} label>
					{#each readinessBuckets as entry, index}
						<Cell fill={COLORS[index % COLORS.length]} />
					{/each}
				</Pie>
				<Tooltip />
			</PieChart>
		</ResponsiveContainer>
	</div>

	<!-- Recommendation Breakdown -->
	<div class="rounded-xl bg-white p-4 shadow">
		<h3 class="mb-2 text-lg font-semibold text-slate-700">Recommendation Breakdown</h3>
		<ResponsiveContainer width="100%" height={250}>
			<BarChart data={recommendationCounts}>
				<CartesianGrid strokeDasharray="3 3" />
				<XAxis dataKey="name" />
				<YAxis />
				<Tooltip />
				<Bar dataKey="value" fill="#156B7D" radius={[8, 8, 0, 0]} />
			</BarChart>
		</ResponsiveContainer>
	</div>

	<!-- Status Overview -->
	<div class="rounded-xl bg-white p-4 shadow">
		<h3 class="mb-2 text-lg font-semibold text-slate-700">Fleet Status</h3>
		<ResponsiveContainer width="100%" height={250}>
			<BarChart data={statusCounts}>
				<CartesianGrid strokeDasharray="3 3" />
				<XAxis dataKey="name" />
				<YAxis />
				<Tooltip />
				<Bar dataKey="value" fill="#82C24B" radius={[8, 8, 0, 0]} />
			</BarChart>
		</ResponsiveContainer>
	</div>
</div>
