import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	try {
		// Forward the uploaded file to your ngrok FastAPI server
		const formData = await request.formData();

		const upstreamResponse = await fetch('https://8b4d6db23391.ngrok-free.app/predict_csv/', {
			method: 'POST',
			body: formData,
			// only needed if ngrok blocks server requests with banner
			headers: { 'ngrok-skip-browser-warning': 'true' }
		});

		if (!upstreamResponse.ok) {
			const errText = await upstreamResponse.text();
			return new Response(errText, {
				status: upstreamResponse.status
			});
		}

		// Pass the CSV response back to the frontend
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
