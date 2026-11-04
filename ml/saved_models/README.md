# ML Saved Models Directory

This folder is the designated storage directory for trained machine learning model artifacts:

1. `plant_disease_model.h5` / `plant_disease_model.keras`
   - TensorFlow/Keras CNN or ResNet-50 weights for plant disease classification.
2. `crop_recommendation_model.pkl` / `crop_recommendation_model.joblib`
   - Scikit-learn Random Forest or XGBoost pipeline trained on location, agro-climatic, soil, and water features.

When placed here, the AgriSaathi backend automatically discovers and loads the trained weights.
In the 40% milestone, the backend detects if weights are missing and serves truthful, transparent fallback states.

