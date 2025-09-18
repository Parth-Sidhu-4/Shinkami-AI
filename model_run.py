import pandas as pd
import joblib

# ======================
# Load the saved model
# ======================
pipeline = joblib.load("prob_use_model.pkl")

# ======================
# Load new data from CSV
# ======================
# Example: "new_metro_data.csv"
new_data = pd.read_csv("sample_dataset_for_testing.csv")

# Drop the same columns we excluded during training
drop_cols = [
    'date', 'train_id', 
    'probability_of_use',   # target (not available in new data normally)
    'final_score', 'probability_rank', 'recommendation', 'rank_score'
]
new_data_features = new_data.drop(columns=[c for c in drop_cols if c in new_data.columns])

# ======================
# Predict probability_of_use
# ======================
predictions = pipeline.predict(new_data_features)

# Add predictions back to the dataframe
new_data['predicted_probability_of_use'] = predictions

# ======================
# Save results to new CSV
# ======================
new_data.to_csv("predicted_metro_data.csv", index=False)
print("✅ Predictions saved to predicted_metro_data.csv")