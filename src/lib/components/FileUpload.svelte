<script lang="ts">
	export let onUpload: (file: File) => void;

	let fileInput: HTMLInputElement;

	function handleChange() {
		if (fileInput?.files?.length) {
			const file = fileInput.files[0];
			onUpload(file);
		}
	}

	function triggerSelect() {
		fileInput.click();
	}
</script>

<div class="flex items-center space-x-2">
	<!-- Hidden file input -->
	<input type="file" accept=".csv" bind:this={fileInput} on:change={handleChange} class="hidden" />

	<!-- Single button: pick + upload -->
	<button
		type="button"
		on:click={triggerSelect}
		class="flex transform items-center space-x-2 rounded-xl bg-gradient-to-r from-[#156B7D] to-[#56A8A5] px-5 py-2.5 text-sm font-semibold text-white shadow-md transition hover:scale-105 hover:shadow-lg"
	>
		<!-- Upload Icon -->
		<svg
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
			stroke-width="2"
			stroke="currentColor"
			class="h-5 w-5"
		>
			<path stroke-linecap="round" stroke-linejoin="round" d="M12 16V4m0 0l-4 4m4-4l4 4m-8 8h8" />
		</svg>
		<span>Upload File</span>
	</button>
</div>
