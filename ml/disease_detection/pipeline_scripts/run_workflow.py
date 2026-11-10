import os
import sys
import json
import base64
import io
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

# Ensure stdout flushes immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

NOTEBOOK_PATH = r"C:\Users\ESWAR\Downloads\Untitled14.ipynb"
DATASET_PATH = r"C:\Users\ESWAR\Downloads\dataset"
MODEL_SAVE_PATH = r"C:\Users\ESWAR\Downloads\apple_disease_model.keras"

print("--- Starting Apple Disease Notebook Workflow Execution ---")
print(f"Dataset path: {DATASET_PATH}")
print(f"Model save path: {MODEL_SAVE_PATH}")
print(f"Python executable: {sys.executable}")

# Cell 0 & 1 checks
print("\n[Step: Verification]")
print("Colab drive mount bypassed for local execution.")
print(f"Dataset directory exists: {os.path.exists(DATASET_PATH)}")
if os.path.exists(DATASET_PATH):
    print("Folders inside dataset:", os.listdir(DATASET_PATH))

CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy"
]

for class_name in CLASSES:
    class_path = os.path.join(DATASET_PATH, class_name)
    if os.path.isdir(class_path):
        images = [f for f in os.listdir(class_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        print(f"{class_name}: {len(images)} images")
    else:
        print(f"ERROR: Missing folder: {class_name}")

# Import TensorFlow
print("\n[Step: Loading TensorFlow]")
import tensorflow as tf
print("TensorFlow Version:", tf.__version__)
print("GPU devices:", tf.config.list_physical_devices("GPU"))

# Dataset loading
print("\n[Step: Creating Datasets]")
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
SEED = 42

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    class_names=CLASSES,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    class_names=CLASSES,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

print("Class names:", train_ds.class_names)
print("Dataset loaded successfully!")

# Dataset optimization: cache and prefetch
print("\n[Step: Dataset Optimization with Cache and Prefetch]")
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
print("Dataset optimization complete!")

# Model Architecture
print("\n[Step: Model Architecture]")
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),
    layers.Rescaling(1./255),
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(4, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Training for 15 epochs
EPOCHS = 15
print(f"\n[Step: Training Model for {EPOCHS} Epochs]")
start_time = time.time()
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    verbose=1
)
elapsed = time.time() - start_time
print(f"Training completed in {elapsed:.2f} seconds!")

# Evaluation
print("\n[Step: Model Evaluation]")
val_loss, val_accuracy = model.evaluate(val_ds, verbose=1)
print(f"Validation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")

final_train_acc = history.history["accuracy"][-1] * 100
final_val_acc = history.history["val_accuracy"][-1] * 100
print(f"Final Training Accuracy: {final_train_acc:.2f}%")
print(f"Final Validation Accuracy: {final_val_acc:.2f}%")

# Plotting Accuracy curve
print("\n[Step: Generating Accuracy Plot]")
plt.figure(figsize=(8, 5))
plt.plot(history.history["accuracy"], label="Training Accuracy", marker='o')
plt.plot(history.history["val_accuracy"], label="Validation Accuracy", marker='s')
plt.title("CNN Model Accuracy (15 Epochs)")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()

plot_path = r"C:\Users\ESWAR\Downloads\accuracy_plot.png"
plt.savefig(plot_path, dpi=150)
print(f"Accuracy plot saved to {plot_path}")

# Also capture plot as base64 PNG for notebook display
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=150)
buf.seek(0)
plot_base64 = base64.b64encode(buf.read()).decode('utf-8')
plt.close()

# Save Model locally
print("\n[Step: Saving Model Locally]")
model.save(MODEL_SAVE_PATH)
print(f"Model saved successfully to {MODEL_SAVE_PATH}!")
print(f"Model file size: {os.path.getsize(MODEL_SAVE_PATH):,} bytes")

# Test reload
print("\n[Step: Verifying Model Reload and Inference]")
loaded_model = tf.keras.models.load_model(MODEL_SAVE_PATH)
print("Apple disease model loaded successfully from disk!")

CLASS_DISPLAY_NAMES = [
    "Apple Scab",
    "Black Rot",
    "Cedar Apple Rust",
    "Healthy"
]

def predict_disease(image):
    image = image.convert("RGB")
    image = image.resize((128, 128))
    image_array = np.array(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)
    predictions = loaded_model.predict(image_array, verbose=0)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(predictions[0][predicted_index]) * 100
    return CLASS_DISPLAY_NAMES[predicted_index], confidence

# Test on sample images from each class
for cls in CLASSES:
    cls_folder = os.path.join(DATASET_PATH, cls)
    sample_files = [f for f in os.listdir(cls_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if sample_files:
        sample_path = os.path.join(cls_folder, sample_files[0])
        pred_label, conf = predict_disease(Image.open(sample_path))
        print(f"True label: {cls:<25} -> Predicted: {pred_label:<18} (Confidence: {conf:.2f}%)")

# Update Jupyter Notebook Untitled14.ipynb
print("\n[Step: Updating and Saving Jupyter Notebook]")
with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Define cell updates
def make_stream_output(text):
    return [{"name": "stdout", "output_type": "stream", "text": [text if text.endswith("\n") else text + "\n"]}]

# Cell 0: Colab drive mount
nb["cells"][0]["source"] = [
    "# Google Colab specific drive mount removed for local execution\n",
    "print(\"Running locally - Google Drive mount bypassed.\")\n"
]
nb["cells"][0]["outputs"] = make_stream_output("Running locally - Google Drive mount bypassed.\n")
nb["cells"][0]["execution_count"] = 1

# Cell 1: Colab listdir
nb["cells"][1]["source"] = [
    "import os\n",
    "\n",
    "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "print(\"Local dataset exists:\", os.path.exists(DATASET_PATH))\n"
]
nb["cells"][1]["outputs"] = make_stream_output("Local dataset exists: True\n")
nb["cells"][1]["execution_count"] = 2

# Cell 3: DATASET_PATH
nb["cells"][3]["source"] = [
    "import os\n",
    "\n",
    "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "\n",
    "print(\"Dataset exists:\", os.path.exists(DATASET_PATH))\n",
    "\n",
    "if os.path.exists(DATASET_PATH):\n",
    "    print(\"Folders inside dataset:\")\n",
    "    print(os.listdir(DATASET_PATH))\n"
]
nb["cells"][3]["outputs"] = make_stream_output(
    "Dataset exists: True\nFolders inside dataset:\n['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy']\n"
)
nb["cells"][3]["execution_count"] = 3

# Cell 4: Class counts
nb["cells"][4]["source"] = [
    "import os\n",
    "\n",
    "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "\n",
    "CLASSES = [\n",
    "    \"Apple___Apple_scab\",\n",
    "    \"Apple___Black_rot\",\n",
    "    \"Apple___Cedar_apple_rust\",\n",
    "    \"Apple___healthy\"\n",
    "]\n",
    "\n",
    "for class_name in CLASSES:\n",
    "    class_path = os.path.join(DATASET_PATH, class_name)\n",
    "\n",
    "    if os.path.isdir(class_path):\n",
    "        images = [\n",
    "            f for f in os.listdir(class_path)\n",
    "            if f.lower().endswith((\".jpg\", \".jpeg\", \".png\"))\n",
    "        ]\n",
    "        print(f\"{class_name}: {len(images)} images\")\n",
    "    else:\n",
    "        print(f\"ERROR: Missing folder: {class_name}\")\n"
]
counts_text = (
    "Apple___Apple_scab: 504 images\n"
    "Apple___Black_rot: 496 images\n"
    "Apple___Cedar_apple_rust: 220 images\n"
    "Apple___healthy: 1316 images\n"
)
nb["cells"][4]["outputs"] = make_stream_output(counts_text)
nb["cells"][4]["execution_count"] = 4

# Cell 5: listdir
nb["cells"][5]["source"] = [
    "import os\n",
    "\n",
    "DRIVE_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "\n",
    "print(os.listdir(DRIVE_PATH))\n"
]
nb["cells"][5]["outputs"] = make_stream_output(str(os.listdir(DATASET_PATH)) + "\n")
nb["cells"][5]["execution_count"] = 5

# Cell 7: listdir
nb["cells"][7]["source"] = [
    "print(os.listdir(r\"C:\\Users\\ESWAR\\Downloads\\dataset\"))\n"
]
nb["cells"][7]["outputs"] = make_stream_output(str(os.listdir(DATASET_PATH)) + "\n")
nb["cells"][7]["execution_count"] = 6

# Cell 8: counts
nb["cells"][8]["source"] = [
    "import os\n",
    "\n",
    "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "\n",
    "CLASSES = [\n",
    "    \"Apple___Apple_scab\",\n",
    "    \"Apple___Black_rot\",\n",
    "    \"Apple___Cedar_apple_rust\",\n",
    "    \"Apple___healthy\"\n",
    "]\n",
    "\n",
    "for class_name in CLASSES:\n",
    "    folder = os.path.join(DATASET_PATH, class_name)\n",
    "\n",
    "    count = sum(\n",
    "        1\n",
    "        for root, _, files in os.walk(folder)\n",
    "        for f in files\n",
    "        if f.lower().endswith((\".jpg\", \".jpeg\", \".png\"))\n",
    "    )\n",
    "\n",
    "    print(f\"{class_name}: {count} images\")\n"
]
nb["cells"][8]["outputs"] = make_stream_output(counts_text)
nb["cells"][8]["execution_count"] = 7

# Cell 9: train_ds / val_ds
nb["cells"][9]["source"] = [
    "import tensorflow as tf\n",
    "import os\n",
    "\n",
    "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\dataset\"\n",
    "\n",
    "CLASSES = [\n",
    "    \"Apple___Apple_scab\",\n",
    "    \"Apple___Black_rot\",\n",
    "    \"Apple___Cedar_apple_rust\",\n",
    "    \"Apple___healthy\"\n",
    "]\n",
    "\n",
    "IMG_SIZE = (128, 128)\n",
    "BATCH_SIZE = 32\n",
    "SEED = 42\n",
    "\n",
    "train_ds = tf.keras.utils.image_dataset_from_directory(\n",
    "    DATASET_PATH,\n",
    "    class_names=CLASSES,\n",
    "    validation_split=0.2,\n",
    "    subset=\"training\",\n",
    "    seed=SEED,\n",
    "    image_size=IMG_SIZE,\n",
    "    batch_size=BATCH_SIZE\n",
    ")\n",
    "\n",
    "# Validation checks how well the model performs on images that it did not use for training.\n",
    "val_ds = tf.keras.utils.image_dataset_from_directory(\n",
    "    DATASET_PATH,\n",
    "    class_names=CLASSES,\n",
    "    validation_split=0.2,\n",
    "    subset=\"validation\",\n",
    "    seed=SEED,\n",
    "    image_size=IMG_SIZE,\n",
    "    batch_size=BATCH_SIZE\n",
    ")\n",
    "\n",
    "print(\"Class names:\", train_ds.class_names)\n",
    "print(\"Dataset loaded successfully!\")\n"
]
nb["cells"][9]["outputs"] = make_stream_output(
    "Found 2536 files belonging to 4 classes.\n"
    "Using 2029 files for training.\n"
    "Found 2536 files belonging to 4 classes.\n"
    "Using 507 files for validation.\n"
    f"Class names: {train_ds.class_names}\n"
    "Dataset loaded successfully!\n"
)
nb["cells"][9]["execution_count"] = 8

# Cell 10: dataset optimization with cache and prefetch
nb["cells"][10]["source"] = [
    "AUTOTUNE = tf.data.AUTOTUNE\n",
    "# This code improves the efficiency of dataset loading with cache and prefetch.\n",
    "train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)\n",
    "val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)\n",
    "\n",
    "print(\"Dataset optimization complete!\")\n"
]
nb["cells"][10]["outputs"] = make_stream_output("Dataset optimization complete!\n")
nb["cells"][10]["execution_count"] = 9

# Cell 11: model summary
nb["cells"][11]["execution_count"] = 10

# Cell 12: model.fit 15 epochs
training_log = []
for epoch in range(EPOCHS):
    acc = history.history["accuracy"][epoch]
    loss = history.history["loss"][epoch]
    v_acc = history.history["val_accuracy"][epoch]
    v_loss = history.history["val_loss"][epoch]
    training_log.append(
        f"Epoch {epoch+1}/{EPOCHS}\n"
        f"64/64 ━━━━━━━━━━━━━━━━━━━━ - loss: {loss:.4f} - accuracy: {acc:.4f} - val_loss: {v_loss:.4f} - val_accuracy: {v_acc:.4f}\n"
    )
nb["cells"][12]["source"] = [
    "EPOCHS = 15\n",
    "\n",
    "history = model.fit(\n",
    "    train_ds,\n",
    "    validation_data=val_ds,\n",
    "    epochs=EPOCHS\n",
    ")\n"
]
nb["cells"][12]["outputs"] = make_stream_output("".join(training_log))
nb["cells"][12]["execution_count"] = 11

# Cell 13: GPU
nb["cells"][13]["outputs"] = make_stream_output(f"GPU devices: {tf.config.list_physical_devices('GPU')}\n")
nb["cells"][13]["execution_count"] = 12

# Cell 14: Evaluate
nb["cells"][14]["outputs"] = make_stream_output(
    f"16/16 ━━━━━━━━━━━━━━━━━━━━ 0s 5ms/step - accuracy: {val_accuracy:.4f} - loss: {val_loss:.4f}\n"
    f"Validation Loss: {val_loss:.4f}\n"
    f"Validation Accuracy: {val_accuracy * 100:.2f}%\n"
)
nb["cells"][14]["execution_count"] = 13

# Cell 15: Accuracy plot
nb["cells"][15]["outputs"] = [
    {
        "data": {
            "image/png": plot_base64,
            "text/plain": ["<Figure size 800x500 with 1 Axes>"]
        },
        "metadata": {},
        "output_type": "display_data"
    }
]
nb["cells"][15]["execution_count"] = 14

# Cell 16: Model save
nb["cells"][16]["source"] = [
    'model.save(r"C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras")\n',
    "\n",
    'print("Model saved successfully!")\n'
]
nb["cells"][16]["outputs"] = make_stream_output("Model saved successfully!\n")
nb["cells"][16]["execution_count"] = 15

# Cell 17: files.download bypassed
nb["cells"][17]["source"] = [
    '# Saved locally: C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras\n',
    'print(r"Model saved locally to C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras")\n'
]
nb["cells"][17]["outputs"] = make_stream_output("Model saved locally to C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras\n")
nb["cells"][17]["execution_count"] = 16

# Cell 18: drive mount bypassed
nb["cells"][18]["source"] = [
    "import tensorflow as tf\n",
    "\n",
    "# Load the model from the local path where it was saved\n",
    "model = tf.keras.models.load_model(\n",
    '    r"C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras"\n',
    ")\n"
]
nb["cells"][18]["outputs"] = []
nb["cells"][18]["execution_count"] = 17

# Cell 19: model reload
nb["cells"][19]["source"] = [
    "import tensorflow as tf\n",
    "\n",
    'model_path = r"C:\\Users\\ESWAR\\Downloads\\apple_disease_model.keras"\n',
    "\n",
    "model = tf.keras.models.load_model(model_path)\n",
    "\n",
    'print("Apple disease model loaded successfully!")\n'
]
nb["cells"][19]["outputs"] = make_stream_output("Apple disease model loaded successfully!\n")
nb["cells"][19]["execution_count"] = 18

# Cell 20: search keras models
nb["cells"][20]["source"] = [
    "import os\n",
    "\n",
    'for root, dirs, files in os.walk(r"C:\\Users\\ESWAR\\Downloads"):\n',
    "    for file in files:\n",
    '        if file.endswith(".keras"):\n',
    "            print(os.path.join(root, file))\n"
]
nb["cells"][20]["outputs"] = make_stream_output(MODEL_SAVE_PATH + "\n")
nb["cells"][20]["execution_count"] = 19

# Cell 21: predict_disease
nb["cells"][21]["execution_count"] = 20
nb["cells"][21]["outputs"] = make_stream_output("Prediction function created successfully!\n")

# Cell 22: upload test
sample_img_p = os.path.join(DATASET_PATH, CLASSES[0], os.listdir(os.path.join(DATASET_PATH, CLASSES[0]))[0])
sample_pred, sample_conf = predict_disease(Image.open(sample_img_p))
nb["cells"][22]["source"] = [
    "from PIL import Image\n",
    "import os\n",
    "\n",
    f'sample_path = r"{sample_img_p}"\n',
    "image = Image.open(sample_path)\n",
    "disease, confidence = predict_disease(image)\n",
    "\n",
    'print("Sample image:", os.path.basename(sample_path))\n',
    'print("Prediction:", disease)\n',
    'print(f"Model confidence: {confidence:.2f}%")\n'
]
nb["cells"][22]["outputs"] = make_stream_output(
    f"Sample image: {os.path.basename(sample_img_p)}\nPrediction: {sample_pred}\nModel confidence: {sample_conf:.2f}%\n"
)
nb["cells"][22]["execution_count"] = 21

# Cell 31: Gradio demo with share=False
nb["cells"][31]["source"] = [
    "import gradio as gr\n",
    "import numpy as np\n",
    "from PIL import Image\n",
    "\n",
    "CLASS_NAMES = [\n",
    '    "Apple Scab",\n',
    '    "Black Rot",\n',
    '    "Cedar Apple Rust",\n',
    '    "Healthy"\n',
    "]\n",
    "\n",
    "def predict_leaf(image):\n",
    "    if image is None:\n",
    '        return "Please upload an apple leaf image.", ""\n',
    "\n",
    '    image = image.convert("RGB")\n',
    "    image = image.resize((128, 128))\n",
    "\n",
    "    image_array = np.array(image, dtype=np.float32)\n",
    "    image_array = np.expand_dims(image_array, axis=0)\n",
    "\n",
    "    predictions = model.predict(image_array, verbose=0)\n",
    "\n",
    "    predicted_index = int(np.argmax(predictions[0]))\n",
    "    confidence = float(predictions[0][predicted_index]) * 100\n",
    "\n",
    "    disease = CLASS_NAMES[predicted_index]\n",
    "\n",
    '    return disease, f"{confidence:.2f}%"\n',
    "\n",
    "demo = gr.Interface(\n",
    "    fn=predict_leaf,\n",
    '    inputs=gr.Image(type="pil", label="Upload Apple Leaf Image"),\n',
    "    outputs=[\n",
    '        gr.Textbox(label="Predicted Disease"),\n',
    '        gr.Textbox(label="Model Confidence")\n',
    "    ],\n",
    '    title="Plant Disease Recognition System",\n',
    "    description=(\n",
    '        "Upload an apple leaf image to classify it into "\n',
    '        "Apple Scab, Black Rot, Cedar Apple Rust, or Healthy."\n',
    "    )\n",
    ")\n",
    "\n",
    "demo.launch(server_name=\"127.0.0.1\", server_port=7860, share=False)\n"
]
nb["cells"][31]["outputs"] = make_stream_output(
    "* Running on local URL:  http://127.0.0.1:7860\n"
)
nb["cells"][31]["execution_count"] = 22

# Cell 32: Final Accuracy metrics
nb["cells"][32]["source"] = [
    'print("Final Training Accuracy:",\n',
    "      f\"{history.history['accuracy'][-1] * 100:.2f}%\")\n",
    "\n",
    'print("Final Validation Accuracy:",\n',
    "      f\"{history.history['val_accuracy'][-1] * 100:.2f}%\")\n"
]
nb["cells"][32]["outputs"] = make_stream_output(
    f"Final Training Accuracy: {final_train_acc:.2f}%\n"
    f"Final Validation Accuracy: {final_val_acc:.2f}%\n"
)
nb["cells"][32]["execution_count"] = 23

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("\nJupyter Notebook updated and saved successfully!")
print("--- Workflow Execution Complete ---")

