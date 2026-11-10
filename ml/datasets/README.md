# Datasets Directory

Store source datasets and training splits for AgriSaathi:

### 1. PlantVillage Multi-Plant Disease Dataset
- **Archive**: `ml/datasets/archive.zip` (857 MB)
- **Extracted Directory**: `ml/datasets/plant_dataset/` (54,304 images across 38 class directories)
- **Supported Crops**: Apple, Blueberry, Cherry, Corn (Maize), Grape, Orange, Peach, Pepper (Bell), Potato, Raspberry, Soybean, Squash, Strawberry, Tomato.
- **Model Target**: Used for training the 38-class Convolutional Neural Network model saved at `ml/saved_models/full_plant_disease_model.keras`.

### 2. Location & Agro-Climatic Datasets
- ICAR regional crop yield & climate datasets (for location-based crop recommendation).
- Soil survey profile dataset (for district/zone soil series classification).
