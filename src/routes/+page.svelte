<script lang="ts">
	import { goto } from '$app/navigation';
	import { auth } from '$lib/utils/firebase';
	import { onAuthStateChanged, signOut } from 'firebase/auth';
	import { onMount } from 'svelte';
	import Reveal from '$lib/components/Reveal.svelte';

	// State for mobile menu
	let isMenuOpen = false;

	// Initial user state is undefined for loading
	let user: any;

	onMount(() => {
		onAuthStateChanged(auth, (u) => {
			user = u;
		});
	});

	async function handleLogout() {
		await signOut(auth);
		goto('/');
	}

	const team = [
		{
			name: 'Parth Sidhu',
			role: 'Team Lead & Developer',
			avatar: 'https://i.ibb.co/CKzzttDT/Parth-Sidhu.jpg'
		},
		{
			name: 'Nikhil Rathaur',
			role: 'Model Training',
			avatar: 'https://i.ibb.co/fgmTxdS/Nikhil-Rathaur.jpg'
		},
		{ name: 'Suwarn', role: 'Research', avatar: 'https://i.ibb.co/VcNSkvqy/Suwarn.jpg' },
		{
			name: 'Priya Gupta',
			role: 'Research and Presentation',
			avatar: 'https://i.ibb.co/Cp9MQcWj/Priya.jpg'
		},
		{
			name: 'Aryan Vaish',
			role: 'Testing and Support',
			avatar: 'https://i.ibb.co/Z1GWwPkk/Aryan-Vaish.jpg'
		},
		{ name: 'Sumit Kumar', role: 'Support', avatar: 'https://i.ibb.co/hxytXDq6/Sumit-Kumar.jpg' }
	];
	const mentor = {
		name: 'Dr. Anshika Srivastava',
		role: 'Faculty Mentor',
		avatar: 'https://i.ibb.co/NT1B7nJ/1703908262735.jpg'
	};
	const specialThanks = {
		name: 'Dr. Vipul Kumar Mishra',
		role: 'Advisor',
		avatar: 'https://i.ibb.co/XfHY3YYy/Dr-Vipul-Kumar-Mishra.jpg'
	};
	const technologies = [
		{
			name: 'SvelteKit',
			logo: 'https://raw.githubusercontent.com/sveltejs/branding/master/svelte-logo.svg',
			desc: 'Frontend framework for reactive UI.'
		},
		{
			name: 'TailwindCSS',
			logo: 'https://www.vectorlogo.zone/logos/tailwindcss/tailwindcss-icon.svg',
			desc: 'Utility-first CSS framework for styling.'
		},
		{
			name: 'FastAPI',
			logo: 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/fastapi.svg',
			desc: 'Python API framework for ML predictions.'
		},
		{
			name: 'ngrok',
			logo: 'https://images.icon-icons.com/3913/PNG/512/ngrok_logo_icon_248373.png',
			desc: 'Securely exposes the local API to the web.'
		},
		{
			name: 'Scikit-learn',
			logo: 'https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg',
			desc: 'Machine learning library for model training.'
		},
		{
			name: 'Firebase',
			logo: 'https://www.vectorlogo.zone/logos/firebase/firebase-icon.svg',
			desc: 'Authentication & backend services.'
		},
		{
			name: 'Vercel',
			logo: 'https://www.vectorlogo.zone/logos/vercel/vercel-icon.svg',
			desc: 'Frontend deployment & hosting.'
		}
	];
	const workflow = [
		{
			icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#156B7D]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v4h16v-4M4 12l8-8 8 8" /></svg>`,
			label: 'CSV Upload',
			step: 'Step 1',
			desc: 'Upload train operation data in CSV format.'
		},
		{
			icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#156B7D]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>`,
			label: 'API & Model',
			step: 'Step 2',
			desc: 'Run ML pipelines via FastAPI backend.'
		},
		{
			icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#156B7D]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 11V7h2v4h3l-4 4-4-4h3z" /></svg>`,
			label: 'Predictions',
			step: 'Step 3',
			desc: 'AI generates readiness & maintenance predictions.'
		},
		{
			icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#156B7D]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><rect x="3" y="3" width="18" height="18" rx="2" ry="2" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9h18" /></svg>`,
			label: 'Dashboard',
			step: 'Step 4',
			desc: 'Interactive UI displays insights to planners.'
		}
	];
	const methodology = [
		{
			title: 'Dataset Collection',
			desc: 'Operational data is gathered in a standardized CSV format for processing.'
		},
		{
			title: 'Data Preprocessing',
			desc: 'Data is cleaned, and features are engineered, encoded, and scaled for the model.'
		},
		{
			title: 'Model Training',
			desc: 'A Gradient Boosting Regressor is trained on historical data to learn patterns.'
		},
		{
			title: 'API Deployment',
			desc: 'The trained model is served via a high-performance FastAPI backend for real-time predictions.'
		},
		{
			title: 'Dashboard Integration',
			desc: 'The frontend visualizes predictions, enabling planners to make informed decisions.'
		}
	];
</script>

<div class="flex min-h-screen flex-col bg-gray-50 text-slate-800">
	<nav
		class="sticky top-0 z-50 flex items-center justify-between bg-white/80 px-4 py-3 shadow-sm backdrop-blur-lg md:px-8"
	>
		<a href="/" class="flex items-center space-x-3">
			<img
				src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
				alt="Shinkami AI Logo"
				class="h-12 w-12 rounded-lg"
				width="48"
				height="48"
			/>
			<span
				class="bg-gradient-to-r from-[#156B7D] via-[#56A8A5] to-[#82C24B] bg-clip-text text-2xl font-black tracking-tighter text-transparent"
				style="font-family: 'Montserrat', sans-serif;"
			>
				Shinkami AI
			</span>
		</a>

		<div class="hidden items-center space-x-2 sm:flex md:space-x-4">
			<a
				href="#why"
				class="rounded-lg px-3 py-2 font-medium text-slate-600 transition-colors duration-300 hover:text-[#156B7D]"
			>
				Why Shinkami?
			</a>
			<a
				href="#team"
				class="rounded-lg px-3 py-2 font-medium text-slate-600 transition-colors duration-300 hover:text-[#156B7D]"
			>
				Team
			</a>

			{#if user === undefined}
				<div class="h-9 w-28 animate-pulse rounded-lg bg-slate-200"></div>
				<div class="h-9 w-20 animate-pulse rounded-lg bg-slate-200"></div>
			{:else if user}
				<a
					href="/dashboard"
					class="rounded-lg bg-[#156B7D] px-4 py-2 text-sm font-semibold text-white shadow-sm transition-all duration-300 hover:scale-105 hover:bg-[#82C24B]"
				>
					Dashboard
				</a>
				<button
					on:click={handleLogout}
					class="rounded-lg px-4 py-2 text-sm font-semibold text-[#156B7D] ring-1 ring-[#156B7D] transition-colors duration-300 ring-inset hover:bg-[#156B7D] hover:text-white"
				>
					Logout
				</button>
			{:else}
				<a
					href="/login"
					class="rounded-lg px-4 py-2 text-sm font-semibold text-[#156B7D] ring-1 ring-[#156B7D] transition-colors duration-300 ring-inset hover:bg-[#156B7D] hover:text-white"
				>
					Get Started
				</a>
			{/if}
		</div>

		<div class="sm:hidden">
			<button
				on:click={() => (isMenuOpen = !isMenuOpen)}
				class="rounded-md p-2 text-slate-600 hover:bg-slate-100 hover:text-[#156B7D] focus:ring-2 focus:ring-[#156B7D] focus:outline-none focus:ring-inset"
				aria-label="Open main menu"
			>
				{#if isMenuOpen}
					<svg
						class="h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
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
				{:else}
					<svg
						class="h-6 w-6"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16M4 18h16"
						/></svg
					>
				{/if}
			</button>
		</div>
	</nav>

	{#if isMenuOpen}
		<div class="sm:hidden">
			<div class="space-y-1 px-2 pt-2 pb-3">
				<a
					href="#why"
					on:click={() => (isMenuOpen = false)}
					class="block rounded-md px-3 py-2 text-base font-medium text-slate-600 hover:bg-slate-100 hover:text-[#156B7D]"
					>Why Shinkami?</a
				>
				<a
					href="#team"
					on:click={() => (isMenuOpen = false)}
					class="block rounded-md px-3 py-2 text-base font-medium text-slate-600 hover:bg-slate-100 hover:text-[#156B7D]"
					>Team</a
				>
				<div class="border-t border-slate-200 pt-4">
					{#if user === undefined}
						<div class="mx-3 h-10 w-auto animate-pulse rounded-lg bg-slate-200"></div>
					{:else if user}
						<a
							href="/dashboard"
							class="block w-full rounded-lg bg-[#156B7D] px-4 py-2 text-left text-sm font-semibold text-white shadow-sm"
							>Dashboard</a
						>
						<button
							on:click={handleLogout}
							class="mt-2 block w-full rounded-lg px-4 py-2 text-left text-sm font-semibold text-[#156B7D] ring-1 ring-[#156B7D] ring-inset"
							>Logout</button
						>
					{:else}
						<a
							href="/login"
							class="block w-full rounded-lg bg-[#156B7D] px-4 py-2 text-left text-sm font-semibold text-white shadow-sm"
							>Get Started</a
						>
					{/if}
				</div>
			</div>
		</div>
	{/if}

	<section
		class="animated-gradient-bg relative overflow-hidden px-6 py-24 text-white sm:px-10 md:px-20"
	>
		<div
			class="absolute inset-0 bg-[url('/grid.svg')] [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))] bg-center opacity-30"
		></div>

		<div
			class="relative z-10 mx-auto flex max-w-7xl flex-col items-center text-center md:flex-row md:justify-between md:text-left"
		>
			<Reveal class="md:w-6/12">
				<div class="space-y-6">
					<div
						class="inline-block rounded-full border border-teal-500/50 bg-teal-500/10 px-4 py-1.5 text-sm font-semibold text-teal-300"
					>
						Smart India Hackathon 2025
					</div>
					<h1 class="text-4xl font-extrabold tracking-tighter text-white sm:text-5xl md:text-6xl">
						Smarter <span class="text-[#82C24B]">Train Readiness</span><br />with Predictive AI
					</h1>
					<p class="mx-auto max-w-xl text-lg text-slate-300 md:mx-0">
						The Shinkansen from Japan is the global standard for railway precision. Our project, <strong
							>Shinkami</strong
						>, channels this spirit of excellence. Translating to 'divine intelligence' (神上), we
						bring this elevated foresight to Kochi Metro, using predictive AI to attempt train
						readiness with effortless certainty.
					</p>
					<div class="flex flex-wrap justify-center gap-4 md:justify-start">
						<button
							on:click={() => goto(user ? '/dashboard' : '/login')}
							class="transform rounded-lg bg-[#82C24B] px-6 py-3 font-semibold text-slate-900 shadow-lg transition-transform duration-300 hover:scale-105"
						>
							{user ? 'Go to Dashboard' : 'Login & Explore'}
						</button>
						<a
							href="#workflow"
							class="rounded-lg px-6 py-3 font-semibold text-white ring-1 ring-slate-600 transition-colors duration-300 ring-inset hover:bg-slate-800"
						>
							See Workflow
						</a>
					</div>
				</div>
			</Reveal>

			<Reveal class="mt-12 md:mt-0 md:w-5/12">
				<div class="group relative">
					<div
						class="absolute -inset-1 rounded-xl bg-gradient-to-r from-teal-500 to-green-500 opacity-20 blur-xl transition duration-500 group-hover:opacity-50"
					></div>
					<img
						src="https://kochimetro.org/wp-content/uploads/2018/01/train.png"
						alt="Kochi Metro Train"
						class="relative w-full max-w-md rounded-xl shadow-2xl"
						width="512"
						height="325"
					/>
				</div>
			</Reveal>
		</div>
	</section>

	<div class="bg-slate-100 py-12">
		<div
			class="mx-auto grid max-w-4xl grid-cols-1 gap-10 px-4 text-center md:grid-cols-2 md:items-center"
		>
			<div class="flex flex-col items-center">
				<p class="mb-4 text-sm font-semibold tracking-wider text-slate-500 uppercase">Team From</p>
				<a
					href="https://gsv.ac.in/"
					target="_blank"
					rel="noopener noreferrer"
					title="Gati Shakti Vishwavidyalaya"
				>
					<img
						src="https://gsv.ac.in/wp-content/uploads/2024/11/cropped-logo_for_website-1-2.png"
						alt="GSV Logo"
						class="h-12 w-auto invert transition-transform duration-300 hover:scale-105"
						width="150"
						height="48"
					/>
				</a>
			</div>

			<div class="flex flex-col items-center md:border-l md:border-slate-300">
				<p class="mb-4 text-sm font-semibold tracking-wider text-slate-500 uppercase">
					Official Submission For
				</p>
				<a
					href="https://sih.gov.in/"
					target="_blank"
					rel="noopener noreferrer"
					title="Smart India Hackathon"
				>
					<img
						src="https://sih.gov.in/img1/SIH2025-logo.png"
						alt="SIH Logo"
						class="h-12 w-auto transition-transform duration-300 hover:scale-105"
						width="196"
						height="48"
					/>
				</a>
			</div>
		</div>
	</div>

	<section id="why" class="bg-white px-6 py-24 sm:px-10 md:px-20">
		<div class="mx-auto max-w-6xl">
			<Reveal>
				<div class="text-center">
					<h2 class="text-3xl font-extrabold tracking-tighter text-[#156B7D] sm:text-4xl">
						Why Shinkami AI?
					</h2>
					<p class="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
						Transforming daily operations from a manual puzzle into a data-driven strategy.
					</p>
				</div>
			</Reveal>

			<div class="mt-16 grid gap-12 md:grid-cols-2 md:gap-16">
				<Reveal>
					<div class="space-y-4">
						<h3 class="flex items-center gap-3 text-2xl font-bold text-slate-800">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-amber-500"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								><path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
								/></svg
							>
							The Challenge
						</h3>
						<p class="text-slate-600">
							Current manual workflows rely on siloed spreadsheets and logbooks, leading to
							operational inefficiencies and increased risks:
						</p>
						<ul class="space-y-2">
							<li class="flex items-start gap-3">
								<svg
									class="mt-1 h-5 w-5 flex-shrink-0 text-red-500"
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 20 20"
									fill="currentColor"
									><path
										fill-rule="evenodd"
										d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
										clip-rule="evenodd"
									/></svg
								>
								<span
									><strong>Service Risks:</strong> Missed clearances can cause unscheduled rake withdrawals.</span
								>
							</li>
							<li class="flex items-start gap-3">
								<svg
									class="mt-1 h-5 w-5 flex-shrink-0 text-red-500"
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 20 20"
									fill="currentColor"
									><path
										fill-rule="evenodd"
										d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
										clip-rule="evenodd"
									/></svg
								>
								<span
									><strong>Increased Costs:</strong> Uneven mileage distribution accelerates wear and
									maintenance expenses.</span
								>
							</li>
						</ul>
					</div>
				</Reveal>

				<Reveal>
					<div class="space-y-4">
						<h3 class="flex items-center gap-3 text-2xl font-bold text-slate-800">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-8 w-8 text-teal-500"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								><path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
								/></svg
							>
							Our Solution
						</h3>
						<p class="text-slate-600">
							Shinkami AI provides a data-driven, auditable, and reproducible workflow with clear
							benefits:
						</p>
						<ul class="space-y-2">
							<li class="flex items-start gap-3">
								<svg
									class="mt-1 h-5 w-5 flex-shrink-0 text-green-500"
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 20 20"
									fill="currentColor"
									><path
										fill-rule="evenodd"
										d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
										clip-rule="evenodd"
									/></svg
								>
								<span
									><strong>Predictive Power:</strong> Applies rule-based constraints & multi-objective
									optimization.</span
								>
							</li>
							<li class="flex items-start gap-3">
								<svg
									class="mt-1 h-5 w-5 flex-shrink-0 text-green-500"
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 20 20"
									fill="currentColor"
									><path
										fill-rule="evenodd"
										d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
										clip-rule="evenodd"
									/></svg
								>
								<span
									><strong>Explainable AI:</strong> Generates ranked induction lists with clear reasoning
									and conflict alerts.</span
								>
							</li>
						</ul>
						<p
							class="mt-4 rounded-lg bg-teal-50 p-4 font-semibold text-teal-800 ring-1 ring-teal-200 ring-inset"
						>
							Result: Higher fleet availability, lower costs, and freed-up staff for strategic
							decisions.
						</p>
					</div>
				</Reveal>
			</div>
		</div>
	</section>

	<section id="workflow" class="pattern-bg px-6 py-24 sm:px-10 md:px-20">
		<Reveal>
			<div class="text-center">
				<h2 class="text-3xl font-extrabold tracking-tighter text-[#156B7D] sm:text-4xl">
					Dashboard Workflow
				</h2>
				<p class="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
					A simple, four-step process from raw data to actionable insights.
				</p>
			</div>
		</Reveal>
		<div class="relative mx-auto mt-16 grid max-w-5xl gap-10 sm:grid-cols-2 md:grid-cols-4">
			{#each workflow as wf, idx}
				<div class="relative">
					<Reveal>
						<div
							class="group relative flex flex-col items-center rounded-xl border border-slate-200 bg-white p-6 text-center shadow-lg transition duration-300 hover:-translate-y-2 hover:shadow-2xl"
						>
							<div class="mb-4 rounded-full bg-teal-100 p-4 ring-8 ring-teal-50">
								{@html wf.icon}
							</div>
							<p class="font-bold text-slate-800">{wf.label}</p>
							<p class="text-sm font-semibold text-[#56A8A5]">{wf.step}</p>
							<p class="mt-2 text-sm text-slate-500">{wf.desc}</p>
						</div>
					</Reveal>
					{#if idx < workflow.length - 1}
						<div
							aria-hidden="true"
							class="absolute top-1/2 -right-1/2 hidden w-1/2 translate-y-[-50%] lg:block"
						>
							<svg
								class="h-auto w-full text-slate-300"
								preserveAspectRatio="none"
								viewBox="0 0 100 2"
								fill="none"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									stroke-dasharray="4 4"
									stroke-linecap="round"
									d="M0 1H100"
									stroke="currentColor"
									stroke-width="2"
								/>
							</svg>
						</div>
					{/if}
				</div>
			{/each}
		</div>
	</section>

	<section id="tech" class="bg-white px-6 py-24 sm:px-10 md:px-20">
		<Reveal>
			<div class="text-center">
				<h2 class="text-3xl font-extrabold tracking-tighter text-[#156B7D] sm:text-4xl">
					Technology Stack
				</h2>
				<p class="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
					Built with modern, powerful, and scalable technologies.
				</p>
			</div>
		</Reveal>

		<div
			class="mx-auto mt-16 flex max-w-5xl flex-wrap items-center justify-center gap-x-8 gap-y-12"
		>
			{#each technologies as tech}
				<Reveal>
					<div class="group relative flex w-24 flex-col items-center gap-3 text-center">
						<div
							class="relative flex h-20 w-20 items-center justify-center rounded-2xl bg-slate-100 transition duration-300 group-hover:-translate-y-1 group-hover:bg-white group-hover:shadow-lg"
						>
							<img
								src={tech.logo}
								alt={tech.name}
								class="h-10 w-10 object-contain transition-transform duration-300 group-hover:scale-110"
								width="40"
								height="40"
							/>
						</div>
						<p class="font-semibold text-slate-700">{tech.name}</p>

						<div
							class="invisible absolute bottom-full mb-3 w-48 scale-95 transform rounded-md bg-slate-800 px-3 py-2 text-center text-xs font-semibold text-white opacity-0 transition-all duration-300 group-hover:visible group-hover:scale-100 group-hover:opacity-100"
						>
							{tech.desc}
							<div
								class="absolute -bottom-1 left-1/2 h-2 w-2 -translate-x-1/2 rotate-45 bg-slate-800"
							></div>
						</div>
					</div>
				</Reveal>
			{/each}
		</div>
	</section>
	<section id="methodology" class="pattern-bg px-6 py-24 sm:px-10 md:px-20">
		<Reveal>
			<div class="text-center">
				<h2 class="text-3xl font-extrabold tracking-tighter text-[#156B7D] sm:text-4xl">
					Our Methodology
				</h2>
				<p class="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
					A structured approach to ensure accuracy and reliability from start to finish.
				</p>
			</div>
		</Reveal>

		<div class="relative mx-auto mt-16 max-w-3xl">
			<div class="absolute top-4 left-4 h-full w-0.5 bg-slate-200" aria-hidden="true"></div>
			<div class="space-y-12">
				{#each methodology as step, idx}
					<Reveal>
						<div class="relative flex items-start gap-6">
							<div
								class="z-10 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-[#156B7D] font-bold text-white"
							>
								{idx + 1}
							</div>
							<div class="flex-1">
								<h4 class="text-lg font-bold text-slate-800">{step.title}</h4>
								<p class="mt-1 text-slate-600">{step.desc}</p>
							</div>
						</div>
					</Reveal>
				{/each}
			</div>
		</div>
	</section>

	<section id="team" class="bg-white px-6 py-24 sm:px-10 md:px-20">
		<Reveal>
			<div class="text-center">
				<h2 class="text-3xl font-extrabold tracking-tighter text-[#156B7D] sm:text-4xl">
					Our Team & Mentors
				</h2>
				<p class="mx-auto mt-4 max-w-2xl text-lg text-slate-600">
					The minds behind the project, guided by incredible faculty.
				</p>
			</div>
		</Reveal>

		<div class="mx-auto mt-16 grid max-w-6xl gap-8 sm:grid-cols-2 md:grid-cols-3">
			{#each team as member}
				<Reveal>
					<div
						class="group rounded-xl bg-white p-6 text-center shadow-lg transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
					>
						<img
							src={member.avatar}
							alt={member.name}
							class="mx-auto mb-4 h-24 w-24 rounded-full shadow-md transition-transform duration-300 group-hover:scale-105"
							width="96"
							height="96"
						/>
						<h3 class="text-lg font-semibold text-slate-900">{member.name}</h3>
						<p class="text-[#156B7D]">{member.role}</p>
					</div>
				</Reveal>
			{/each}
		</div>

		<div class="mt-20 grid gap-10 md:grid-cols-2 md:gap-16">
			<Reveal>
				<div
					class="flex flex-col items-center rounded-xl bg-slate-50 p-8 text-center ring-1 ring-slate-200"
				>
					<h3 class="mb-4 text-sm font-bold tracking-widest text-slate-500 uppercase">
						Faculty Mentor
					</h3>
					<img
						src={mentor.avatar}
						alt={mentor.name}
						class="mx-auto mb-4 h-28 w-28 rounded-full shadow-lg"
						width="112"
						height="112"
					/>
					<h4 class="text-xl font-bold text-slate-900">{mentor.name}</h4>
					<p class="text-slate-600">{mentor.role}</p>
				</div>
			</Reveal>
			<Reveal>
				<div
					class="flex flex-col items-center rounded-xl bg-slate-50 p-8 text-center ring-1 ring-slate-200"
				>
					<h3 class="mb-4 text-sm font-bold tracking-widest text-slate-500 uppercase">
						Special Thanks
					</h3>
					<img
						src={specialThanks.avatar}
						alt={specialThanks.name}
						class="mx-auto mb-4 h-28 w-28 rounded-full shadow-lg"
						width="112"
						height="112"
					/>
					<h4 class="text-xl font-bold text-slate-900">{specialThanks.name}</h4>
					<p class="text-slate-600">{specialThanks.role}</p>
				</div>
			</Reveal>
		</div>
	</section>

	<footer class="bg-slate-900 text-slate-400">
		<div class="mx-auto max-w-7xl px-8 py-8 text-center text-sm">
			<p>
				&copy; {new Date().getFullYear()} Shinkami AI — A Smart India Hackathon 2025 Submission.
			</p>

			<p class="mt-4 text-slate-500">
				Made with <span class="text-white-500">&hearts;</span> by Parth Sidhu & Nikhil Rathaur
				<br />
				<span class="opacity-80"
					>Electronics & Communication Engineering, Gati Shakti Vishwavidyalaya</span
				>
			</p>

			<p class="mt-4 border-t border-slate-700 pt-4 text-xs opacity-60">
				For academic and demonstration purposes only. Not for commercial use.
			</p>
		</div>
	</footer>
</div>

<style>
	:global(html) {
		scroll-behavior: smooth;
	}
	.pattern-bg {
		background-image: radial-gradient(#d1e8e2 0.5px, transparent 0.5px);
		background-size: 15px 15px;
	}

	/* Change: Animated Gradient Background */
	.animated-gradient-bg {
		background: linear-gradient(45deg, #0f172a, #156b7d, #1e3a8a, #0f172a);
		background-size: 400% 400%;
		animation: gradientAnimation 15s ease infinite;
	}

	@keyframes gradientAnimation {
		0% {
			background-position: 0% 50%;
		}
		50% {
			background-position: 100% 50%;
		}
		100% {
			background-position: 0% 50%;
		}
	}
</style>
