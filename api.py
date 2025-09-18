import pandas as pd
import numpy as np
import joblib
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import uvicorn
import io

# ======================
# Load saved model
# ======================
model_path = "prob_use_model.pkl"
pipeline = joblib.load(model_path)

# ======================
# Define FastAPI app
# ======================
app = FastAPI(title="Metro Prediction API", version="1.0")

# Columns to drop (same as training)
drop_cols = [
    'date', 'train_id',
    'probability_of_use', 'final_score',
    'probability_rank', 'recommendation', 'rank_score'
]

@app.post("/predict_csv/")
async def predict_csv(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV
        contents = await file.read()
        data = pd.read_csv(io.BytesIO(contents))

        # Drop unwanted columns
        X_new = data.drop(columns=[c for c in drop_cols if c in data.columns])

        # Make predictions
        predictions = pipeline.predict(X_new)

        # Attach predictions
        data["predicted_probability_of_use"] = predictions

        # Clean NaN/Inf
        data = data.replace([np.inf, -np.inf], np.nan).fillna(0.0)

        # Save to in-memory CSV
        output = io.StringIO()
        data.to_csv(output, index=False)
        output.seek(0)

        # Return file as download
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=predictions.csv"}
        )

    except Exception as e:
        return {"error": str(e)}

# ======================
# Run API (for local testing)
# ======================
# Run in terminal: uvicorn api:app --reload
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)



# command to run the file and provide the api key to someone else: uvicorn api:app --reload --port 8000
# open a new terminal type this command: ngrok http 8000

# once you have done that you will get an interface like that : Forwarding    https://abcd-1234-5678.ngrok-free.app -> http://localhost:8000

