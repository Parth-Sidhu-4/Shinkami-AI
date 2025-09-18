<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	// Use only what API really provides
	export let recommendedTrains: {
		train_id: string;
		wear_index: number | string;
		shunting_moves_needed: number | string;
		rank_score: number | string;
		recommendation: string;
		predicted_probability_of_use: number | string;
	}[];

	const dispatch = createEventDispatcher<{ close: null }>();

	const closeModal = () => {
		dispatch('close');
	};
</script>

<div
	on:click={closeModal}
	class="bg-opacity-60 fixed inset-0 z-40 flex items-center justify-center bg-black"
>
	<div on:click|stopPropagation class="z-50 w-full max-w-3xl rounded-xl bg-white shadow-2xl">
		<!-- Header -->
		<div class="flex items-center justify-between border-b p-4">
			<h2 class="text-xl font-bold">System Recommendation</h2>
			<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800">
				&times;
			</button>
		</div>

		<!-- Body -->
		<div class="p-6">
			<p class="mb-4 text-sm text-gray-600">
				The following lineup is recommended based on AI model predictions.
			</p>

			<div class="max-h-[60vh] overflow-y-auto">
				<table class="w-full text-left text-sm">
					<thead class="sticky top-0 border-b bg-gray-50">
						<tr class="text-gray-600 uppercase">
							<th class="p-3">Rank</th>
							<th class="p-3">Train ID</th>
							<th class="p-3 text-center">Wear Index</th>
							<th class="p-3 text-center">Shunting Moves</th>
							<th class="p-3 text-center">Readiness %</th>
							<th class="p-3 text-center font-bold">Final Score</th>
							<th class="p-3 text-center">Recommendation</th>
						</tr>
					</thead>
					<tbody>
						{#each recommendedTrains as train, i}
							<tr class="border-b hover:bg-gray-50">
								<td class="p-3 font-bold">{i + 1}</td>
								<td class="p-3 font-mono">{train.train_id}</td>
								<td class="p-3 text-center">{train.wear_index}</td>
								<td class="p-3 text-center">{train.shunting_moves_needed}</td>
								<td class="p-3 text-center">{train.predicted_probability_of_use}</td>
								<td class="p-3 text-center font-bold text-blue-600">
									{train.rank_score}
								</td>
								<td class="p-3 text-center">{train.recommendation}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
