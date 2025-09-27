// src/routes/api/predict/+server.ts
import type { RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async (event) => {
	try {
		// Forward the uploaded CSV to your ngrok FastAPI server
		const formData = await event.request.formData();

		const upstreamResponse = await fetch('https://3fe58d8f9855.ngrok-free.app/predict_csv/', {
			method: 'POST',
			body: formData,
			headers: { 'ngrok-skip-browser-warning': 'true' }
		});

		if (!upstreamResponse.ok) {
			const errText = await upstreamResponse.text();
			return new Response(errText, { status: upstreamResponse.status });
		}

		// Return the CSV response directly to the frontend
		const text = await upstreamResponse.text();
		return new Response(text, {
			headers: {
				'Content-Type': 'text/csv',
				'Cache-Control': 'no-store'
			}
		});
	} catch (err: any) {
		console.error('Proxy error:', err);
		return new Response(`Proxy error: ${err.message}`, { status: 500 });
	}
};
