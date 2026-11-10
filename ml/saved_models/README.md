# ML Saved Models Directory

This folder is the designated storage directory for trained machine learning model artifacts:

1. `full_plant_disease_model.keras` & `class_mapping.json`
   - TensorFlow/Keras CNN Multi-Class Model trained across 38 disease categories and 14 crop varieties (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Bell Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato).
   - Input shape: `(128, 128, 3)` with built-in `Rescaling(1./255)`.
   - Supports both species-filtered diagnosis and global auto-detection.

2. `crop_recommendation_model.pkl` / `crop_recommendation_model.joblib`
   - Scikit-learn Random Forest or XGBoost pipeline trained on location, agro-climatic, soil, and water features.

When placed here, the AgriSaathi backend automatically discovers and loads the trained weights with live inference.
