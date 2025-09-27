import type { RequestHandler, RequestEvent } from './$types';

export const POST: RequestHandler = async (event: RequestEvent) => {
	try {
		// Forward the uploaded file to your ngrok FastAPI server
		const formData = await event.request.formData();

		const upstreamResponse = await fetch('https://8b4d6db23391.ngrok-free.app/predict_csv/', {
			method: 'POST',
			body: formData,
			headers: { 'ngrok-skip-browser-warning': 'true' }
		});

		if (!upstreamResponse.ok) {
			const errText = await upstreamResponse.text();
			return new Response(errText, { status: upstreamResponse.status });
		}

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
