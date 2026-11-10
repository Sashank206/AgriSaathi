import os
import sys
import json
import numpy as np
from PIL import Image
import gradio as gr
import tensorflow as tf

MODEL_PATH = r"C:\Users\ESWAR\Downloads\full_plant_disease_model.keras"
MAPPING_PATH = r"C:\Users\ESWAR\Downloads\class_mapping.json"

print(f"Loading mapping from {MAPPING_PATH}...")
if not os.path.exists(MAPPING_PATH):
    raise FileNotFoundError(f"Mapping file not found at {MAPPING_PATH}")

with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    mapping_data = json.load(f)

class_names = mapping_data["class_names"]
plant_to_classes = mapping_data["plant_to_classes"]
class_to_disease = mapping_data["class_to_disease"]
sorted_plant_list = mapping_data["plants"]

print(f"Loaded {len(sorted_plant_list)} plants and {len(class_names)} classes.")
print(f"Loading trained model from {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

def predict_plant_disease(selected_plant, image):
    if not selected_plant:
        return "⚠️ Please choose a plant/crop first in Step 1.", {}
    if image is None:
        return "⚠️ Please upload a leaf image in Step 2.", {}

    # Preprocess image to (128, 128, 3)
    img = image.convert("RGB").resize((128, 128))
    img_arr = np.expand_dims(np.array(img, dtype=np.float32), axis=0)

    # Model inference across all classes
    raw_preds = model.predict(img_arr, verbose=0)[0]

    # Filter to selected plant classes
    candidate_classes = plant_to_classes.get(selected_plant, [])
    if not candidate_classes:
        return f"Unknown plant '{selected_plant}'.", {}

    candidate_indices = [class_names.index(c) for c in candidate_classes]
    candidate_probs = [float(raw_preds[i]) for i in candidate_indices]

    # Re-normalize filtered probabilities so they sum to 100%
    total_p = sum(candidate_probs)
    if total_p > 0:
        norm_probs = {
            class_to_disease[c]: float(p / total_p)
            for c, p in zip(candidate_classes, candidate_probs)
        }
    else:
        norm_probs = {
            class_to_disease[c]: float(1.0 / len(candidate_classes))
            for c in candidate_classes
        }

    top_condition = max(norm_probs, key=norm_probs.get)
    top_confidence = norm_probs[top_condition] * 100.0

    result_summary = f"{top_condition} ({top_confidence:.1f}% confidence)"
    return result_summary, norm_probs

demo = gr.Interface(
    fn=predict_plant_disease,
    inputs=[
        gr.Dropdown(choices=sorted_plant_list, label="Step 1: Choose Plant / Crop"),
        gr.Image(type="pil", label="Step 2: Upload Leaf Image")
    ],
    outputs=[
        gr.Textbox(label="Predicted Disease / Condition"),
        gr.Label(label="Top Probabilities within Selected Plant", num_top_classes=3)
    ],
    title="🌿 Multi-Plant Disease Diagnosis System",
    description=(
        "Select a crop or plant category from Step 1, upload a leaf photo in Step 2, "
        "and obtain a disease prediction with confidence probabilities tailored specifically to that plant species."
    )
)

if __name__ == "__main__":
    print("Launching Gradio app on http://127.0.0.1:7860 (share=False)...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
