import type { RequestHandler } from './$types';
import type { RequestEvent } from '@sveltejs/kit';
import fs from 'fs';
import path from 'path';

export const POST: RequestHandler = async (event: RequestEvent) => {
	try {
		const data = await event.request.formData();
		const file = data.get('file') as File | null;

		if (!file) {
			return new Response('No file provided', { status: 400 });
		}

		// Convert to buffer
		const buffer = Buffer.from(await file.arrayBuffer());

		// Save in /static/uploads/
		const uploadDir = path.join(process.cwd(), 'static', 'uploads');
		if (!fs.existsSync(uploadDir)) {
			fs.mkdirSync(uploadDir, { recursive: true });
		}

		const uploadPath = path.join(uploadDir, file.name);
		fs.writeFileSync(uploadPath, buffer);

		return new Response(
			JSON.stringify({
				message: 'File uploaded successfully',
				path: `/uploads/${file.name}`
			}),
			{ status: 200, headers: { 'Content-Type': 'application/json' } }
		);
	} catch (err) {
		console.error('Upload error:', err);
		return new Response('Internal Server Error', { status: 500 });
	}
};
