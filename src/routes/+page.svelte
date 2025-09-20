<script lang="ts">
	import { goto } from '$app/navigation';
	import { auth } from '$lib/utils/firebase';
	import { onAuthStateChanged, signOut } from 'firebase/auth';
	import { onMount } from 'svelte';
	import Reveal from '$lib/components/Reveal.svelte';

	let user: any = null;

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
		{
			name: 'Suwarn',
			role: 'Research',
			avatar: 'https://i.ibb.co/VcNSkvqy/Suwarn.jpg'
		},
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
		{
			name: 'Sumit Kumar',
			role: 'Support',
			avatar: 'https://i.ibb.co/hxytXDq6/Sumit-Kumar.jpg'
		}
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
		{ title: 'Dataset', desc: 'CSV data from daily operations.' },
		{ title: 'Preprocessing', desc: 'Encoding, scaling, missing values handled.' },
		{ title: 'Model Training', desc: 'Gradient Boosting model training.' },
		{ title: 'API', desc: 'FastAPI serves ML predictions.' },
		{ title: 'Dashboard', desc: 'Visualization & decision support.' }
	];
</script>

<div class="flex min-h-screen flex-col bg-white text-[#333333]">
	<!-- Navbar -->
	<nav
		class="sticky top-0 z-50 flex items-center justify-between bg-white/95 px-8 py-4 shadow-md backdrop-blur-md"
	>
		<!-- Logo -->
		<div class="flex items-center space-x-3">
			<img
				src="https://i.ibb.co/qhXCRy8/Gemini-Generated-Image-4aph8l4aph8l4aph.png"
				alt="Shinkami AI Logo"
				class="h-12 w-12 rounded-lg shadow-md"
			/>
			<span
				class="bg-gradient-to-r from-[#156B7D] via-[#56A8A5] to-[#82C24B] bg-clip-text text-2xl font-extrabold tracking-wide text-transparent"
				style="font-family: 'Montserrat', sans-serif;"
			>
				Shinkami AI
			</span>
		</div>

		<!-- Navigation Links -->
		<div class="flex items-center space-x-4 font-medium">
			<a
				href="/"
				class="rounded-lg px-3 py-2 transition hover:bg-[#156B7D]/10 hover:text-[#156B7D]"
			>
				Home
			</a>

			{#if user}
				<a
					href="/dashboard"
					class="rounded-lg bg-[#156B7D] px-3 py-2 font-semibold text-white shadow transition hover:bg-[#82C24B]"
				>
					Dashboard
				</a>
				<button
					on:click={handleLogout}
					class="rounded-lg border border-[#156B7D] px-3 py-2 font-semibold text-[#156B7D] transition hover:bg-[#156B7D] hover:text-white"
				>
					Logout
				</button>
			{:else}
				<a
					href="/login"
					class="rounded-lg bg-[#156B7D] px-3 py-2 font-semibold text-white shadow transition hover:bg-[#82C24B]"
				>
					Login
				</a>
			{/if}
		</div>
	</nav>

	<!-- Hero Section with Logos -->
	<section
		class="relative flex flex-1 flex-col items-center justify-between bg-gradient-to-br from-[#0f172a] via-[#156B7D] to-[#82C24B] px-10 py-20 text-white md:flex-row md:px-20"
	>
		<Reveal>
			<div class="max-w-lg space-y-6 text-center md:text-left">
				<h1 class="text-5xl leading-tight font-extrabold tracking-tight">
					Smarter <span class="text-[#82C24B]">Train Readiness</span><br />with
					<span class="text-[#56A8A5]">AI</span>
				</h1>
				<div
					class="inline-block rounded-full bg-[#82C24B]/20 px-4 py-2 text-sm font-semibold text-[#82C24B] shadow"
				>
					🚀 Smart India Hackathon 2025
				</div>
				<p class="text-lg text-gray-200">
					Shinkami AI helps Kochi Metro Rail Limited ensure daily train availability by predicting
					readiness, recommending maintenance, and optimizing operations with ML.
				</p>
				<div class="flex flex-wrap justify-center gap-4 md:justify-start">
					<button
						on:click={() => goto(user ? '/dashboard' : '/login')}
						class="rounded-lg bg-[#82C24B] px-6 py-3 font-semibold text-white shadow-lg transition hover:bg-[#56A8A5]"
					>
						{user ? 'Go to Dashboard' : 'Login'}
					</button>
					<a
						href="#why"
						class="rounded-lg border border-[#82C24B] px-6 py-3 font-semibold text-[#82C24B] transition hover:bg-[#82C24B]/10"
						>Learn More</a
					>
				</div>

				<!-- Logos Below CTA -->
				<div class="mt-6 flex flex-col items-center gap-4 md:flex-row md:justify-center md:gap-12">
					<!-- SIH Logo -->
					<div class="flex flex-col items-center">
						<img
							src="https://sih.gov.in/img1/SIH2025-logo.png"
							alt="SIH Logo"
							class="h-12 w-auto"
						/>
					</div>

					<!-- Divider (optional) -->
					<div class="hidden h-12 border-l border-gray-300 md:block"></div>

					<!-- GSV Logo -->
					<div class="flex flex-col items-center">
						<img
							src="https://gsv.ac.in/wp-content/uploads/2024/11/cropped-logo_for_website-1-2.png"
							alt="GSV Logo"
							class="h-12 w-auto"
						/>
					</div>
				</div>
			</div>
		</Reveal>
		<Reveal>
			<div class="mt-12 md:mt-0 md:ml-16">
				<img
					src="https://kochimetro.org/wp-content/uploads/2018/01/train.png"
					alt="AI Train Dashboard Illustration"
					class="w-[28rem] rounded-xl border border-white/10 shadow-2xl"
				/>
			</div>
		</Reveal>
	</section>

	<!-- Why Shinkami AI Section -->
	<section id="why" class="bg-white px-10 py-20 md:px-20">
		<h2 class="mb-12 text-center text-3xl font-bold text-[#156B7D]">Why Shinkami AI?</h2>
		<div class="mx-auto grid max-w-6xl gap-12 md:grid-cols-2">
			<!-- Problem -->
			<div class="space-y-4">
				<h3 class="flex items-center gap-2 text-xl font-semibold text-[#156B7D]">
					⚠️ The Challenge
				</h3>
				<p class="text-gray-700">
					Every night, KMRL must decide which of its 25 trainsets enter service, which remain on
					standby, and which go for maintenance. Current manual workflows rely on siloed
					spreadsheets, logbooks, and WhatsApp updates, leading to:
				</p>
				<ul class="ml-6 list-disc space-y-1 text-gray-700">
					<li>Missed clearances risk unscheduled rake withdrawals.</li>
					<li>Uneven mileage accelerates wear & maintenance costs.</li>
					<li>Poor visibility into branding priorities may breach SLAs.</li>
					<li>Excessive night-time shunting increases energy use and safety risk.</li>
				</ul>
			</div>

			<!-- Solution -->
			<div class="space-y-4">
				<h3 class="flex items-center gap-2 text-xl font-semibold text-[#156B7D]">
					✅ How Shinkami Helps
				</h3>
				<p class="text-gray-700">
					Shinkami AI transforms this complex, error-prone process into a **data-driven, auditable,
					and reproducible workflow**:
				</p>
				<ul class="ml-6 list-disc space-y-1 text-gray-700">
					<li>Trained keeping real-world inconsistencies in mind</li>
					<li>Applies rule-based constraints & multi-objective optimization.</li>
					<li>Generates ranked induction lists with explainable reasoning and conflict alerts.</li>
					<li>Learns from historical outcomes via machine-learning feedback loops.</li>
				</ul>
				<p class="mt-2 font-medium text-gray-700">
					Result: Higher fleet availability, lower costs, and freed-up staff for strategic
					decisions.
				</p>
			</div>
		</div>
	</section>

	<!-- Workflow Section -->
	<section id="workflow" class="bg-gray-50 px-10 py-20 md:px-20">
		<h2 class="mb-12 text-center text-3xl font-bold text-[#156B7D]">KMRL Dashboard Workflow</h2>
		<div class="flex flex-col items-center md:flex-row md:justify-center md:space-x-12">
			{#each workflow as wf, idx}
				<Reveal>
					<div class="group relative flex flex-col items-center text-center">
						<div
							class="rounded-2xl bg-white p-6 shadow-lg ring-1 ring-gray-200 transition group-hover:-translate-y-1 group-hover:shadow-xl"
						>
							{@html wf.icon}
							<p class="mt-2 font-semibold">{wf.label}</p>
							<p class="mt-1 text-xs text-gray-500">{wf.step}</p>
						</div>
						<div
							class="absolute top-full mt-2 hidden w-48 rounded-lg bg-black/80 px-3 py-2 text-xs text-white group-hover:block"
						>
							{wf.desc}
						</div>
						{#if idx < workflow.length - 1}
							<svg
								class="absolute top-1/2 left-full hidden h-12 w-24 text-[#56A8A5] md:block"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								viewBox="0 0 100 50"
							>
								<path d="M0,25 Q50,-25 100,25" />
							</svg>
						{/if}
					</div>
				</Reveal>
			{/each}
		</div>
	</section>

	<!-- Technologies Section -->
	<section id="tech" class="bg-white px-10 py-20 md:px-20">
		<h2 class="mb-12 text-center text-3xl font-bold text-[#156B7D]">Technologies Used</h2>
		<div class="grid grid-cols-2 gap-8 text-center sm:grid-cols-3 md:grid-cols-6">
			{#each technologies as tech}
				<Reveal>
					<div
						class="group relative flex flex-col items-center rounded-xl bg-gray-50 p-4 shadow transition hover:shadow-lg"
					>
						<img src={tech.logo} alt={tech.name} class="h-12 w-12 object-contain" />
						<p class="mt-3 text-sm font-medium">{tech.name}</p>
						<div
							class="absolute top-full mt-2 hidden w-48 rounded-lg bg-black/80 px-3 py-2 text-xs text-white group-hover:block"
						>
							{tech.desc}
						</div>
					</div>
				</Reveal>
			{/each}
		</div>
	</section>

	<!-- Methodology Section -->
	<section id="methodology" class="bg-gray-50 px-10 py-20 md:px-20">
		<h2 class="mb-12 text-center text-3xl font-bold text-[#156B7D]">Methodology</h2>
		<div class="grid gap-8 text-center md:grid-cols-5">
			{#each methodology as step}
				<Reveal>
					<div class="group relative rounded-lg bg-white p-4 shadow-sm transition hover:shadow-md">
						<h4 class="font-semibold text-[#156B7D]">{step.title}</h4>
						<p class="text-sm text-gray-600">{step.desc}</p>
						<div
							class="absolute top-full mt-2 hidden w-48 rounded-lg bg-black/80 px-3 py-2 text-xs text-white group-hover:block"
						>
							{step.desc}
						</div>
					</div>
				</Reveal>
			{/each}
		</div>
	</section>

	<!-- Team Section with Mentor & Special Thanks side by side -->
	<section id="team" class="bg-gray-50 px-10 py-20 md:px-20">
		<h2 class="mb-10 text-center text-3xl font-bold text-[#156B7D]">Our Team</h2>

		<!-- Team Members -->
		<div class="grid gap-10 text-center sm:grid-cols-2 md:grid-cols-3">
			{#each team as member}
				<Reveal>
					<div
						class="transform rounded-xl bg-white p-6 shadow transition hover:-translate-y-1 hover:shadow-xl"
					>
						<img
							src={member.avatar}
							alt={member.name}
							class="mx-auto mb-4 w-24 rounded-full shadow"
						/>
						<h3 class="mb-1 text-lg font-semibold text-[#156B7D]">{member.name}</h3>
						<p class="text-sm text-gray-600">{member.role}</p>
					</div>
				</Reveal>
			{/each}
		</div>

		<!-- Mentor & Special Thanks in one row -->
		<Reveal>
			<div class="mt-12 flex flex-col items-center justify-center gap-10 md:flex-row">
				<!-- Mentor Card -->
				<div
					class="w-full max-w-xs rounded-xl border border-[#56A8A5]/30 bg-white p-6 text-center shadow-lg"
				>
					<h3 class="mb-6 text-2xl font-bold text-[#156B7D]">Mentor</h3>
					<img
						src={mentor.avatar}
						alt={mentor.name}
						class="mx-auto mb-4 w-28 rounded-full shadow"
					/>
					<h4 class="mb-1 text-lg font-semibold text-[#156B7D]">{mentor.name}</h4>
					<p class="text-sm text-gray-600">{mentor.role}</p>
				</div>

				<!-- Special Thanks Card -->
				<div
					class="w-full max-w-xs rounded-xl border border-[#56A8A5]/30 bg-white p-6 text-center shadow-lg"
				>
					<h3 class="mb-6 text-2xl font-bold text-[#156B7D]">Special Thanks</h3>
					<img
						src={specialThanks.avatar}
						alt={specialThanks.name}
						class="mx-auto mb-4 w-28 rounded-full shadow"
					/>
					<h4 class="mb-1 text-lg font-semibold text-[#156B7D]">{specialThanks.name}</h4>
					<p class="text-sm text-gray-600">{specialThanks.role}</p>
				</div>
			</div>
		</Reveal>
	</section>

	<!-- Footer -->
	<footer class="bg-[#0f172a] py-6 text-center text-sm text-gray-300">
		Shinkami AI — SIH 2025 | Not for Commercial Purposes | No copyright infringement intended
	</footer>
</div>
