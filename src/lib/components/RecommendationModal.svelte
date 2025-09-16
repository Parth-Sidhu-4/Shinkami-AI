<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { Train } from '$lib/mockData';

	// This component receives the list of scored and sorted trains
	export let recommendedTrains: (Train & { rank_score: number })[];

	const dispatch = createEventDispatcher<{ close: null }>();

	const closeModal = () => {
		dispatch('close');
	};
</script>

<div
	on:click={closeModal}
	class="bg-opacity-60 fixed inset-0 z-40 flex items-center justify-center bg-black"
>
	<div on:click|stopPropagation class="z-50 w-full max-w-2xl rounded-xl bg-white shadow-2xl">
		<div class="flex items-center justify-between border-b p-4">
			<h2 class="text-xl font-bold">System Recommendation</h2>
			<button on:click={closeModal} class="text-2xl text-gray-500 hover:text-gray-800"
				>&times;</button
			>
		</div>

		<div class="p-6">
			<p class="mb-4 text-sm text-gray-600">
				The following lineup is recommended based on balancing low wear, branding needs, and minimal
				shunting.
			</p>
			<div class="max-h-[60vh] overflow-y-auto">
				<table class="w-full text-left text-sm">
					<thead class="sticky top-0 border-b bg-gray-50">
						<tr class="text-gray-600 uppercase">
							<th class="p-3">Rank</th>
							<th class="p-3">Train ID</th>
							<th class="p-3 text-center">Wear Index</th>
							<th class="p-3 text-center">Shunting Moves</th>
							<th class="p-3 text-center font-bold">Final Score</th>
						</tr>
					</thead>
					<tbody>
						{#each recommendedTrains as train, i}
							<tr class="border-b hover:bg-gray-50">
								<td class="p-3 font-bold">{i + 1}</td>
								<td class="p-3 font-mono">{train.train_id}</td>
								<td class="p-3 text-center">{train.wear_index}</td>
								<td class="p-3 text-center">{train.shunting_moves_needed}</td>
								<td class="p-3 text-center font-bold text-blue-600"
									>{train.rank_score.toFixed(1)}</td
								>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</div>
