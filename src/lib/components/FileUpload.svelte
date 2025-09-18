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
		class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold transition hover:bg-blue-500"
	>
		Upload File
	</button>
</div>
