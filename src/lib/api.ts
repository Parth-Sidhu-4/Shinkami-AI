// src/lib/api.ts
export async function getPredictionsFromApi(file: File): Promise<File> {
	const formData = new FormData();
	formData.append('file', file);

	const response = await fetch(
		'https://8b4d6db23391.ngrok-free.app/docs#/default/predict_csv_predict_csv__post',
		{
			method: 'POST',
			body: formData
		}
	);

	if (!response.ok) throw new Error('API request failed');

	// Convert response back into a downloadable File
	const blob = await response.blob();
	return new File([blob], 'predictions.csv', { type: 'text/csv' });
}
