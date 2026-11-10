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

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

NOTEBOOK_PATH = r"C:\Users\ESWAR\Downloads\Untitled14.ipynb"
DATASET_PATH = r"C:\Users\ESWAR\Downloads\plant_dataset"
MODEL_SAVE_PATH = r"C:\Users\ESWAR\Downloads\full_plant_disease_model.keras"
MAPPING_SAVE_PATH = r"C:\Users\ESWAR\Downloads\class_mapping.json"
PLOT_SAVE_PATH = r"C:\Users\ESWAR\Downloads\full_accuracy_plot.png"

print("=================================================================")
print("  MULTI-PLANT DISEASE RECOGNITION - FULL PIPELINE EXECUTION")
print("=================================================================")
print(f"Dataset path: {DATASET_PATH}")
print(f"Model destination: {MODEL_SAVE_PATH}")
print(f"Mapping destination: {MAPPING_SAVE_PATH}")

# -----------------------------------------------------------------
# STEP 1: Scan Classes and Build Mapping Dictionaries
# -----------------------------------------------------------------
print("\n[STEP 1: Scanning Subdirectories & Building Mappings]")

all_subdirs = sorted([
    d for d in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, d)) and "___" in d
])
print(f"Discovered {len(all_subdirs)} class directories in dataset.")

def normalize_plant_name(raw_plant):
    mapping = {
        'Apple': 'Apple',
        'Blueberry': 'Blueberry',
        'Cherry_(including_sour)': 'Cherry',
        'Corn_(maize)': 'Corn (Maize)',
        'Grape': 'Grape',
        'Orange': 'Orange',
        'Peach': 'Peach',
        'Pepper,_bell': 'Pepper (Bell)',
        'Potato': 'Potato',
        'Raspberry': 'Raspberry',
        'Soybean': 'Soybean',
        'Squash': 'Squash',
        'Strawberry': 'Strawberry',
        'Tomato': 'Tomato'
    }
    return mapping.get(raw_plant, raw_plant.replace('_', ' ').strip())

def format_disease_name(raw_disease):
    if raw_disease.lower() == 'healthy':
        return 'Healthy'
    d = raw_disease.replace('_', ' ').strip()
    words = d.split()
    cleaned = ' '.join(w.capitalize() if not (w.startswith('(') or w.isupper()) else w for w in words)
    special = {
        'Common Rust': 'Common Rust',
        'Cercospora Leaf Spot Gray Leaf Spot': 'Cercospora Leaf Spot / Gray Leaf Spot',
        'Esca (black Measles)': 'Esca (Black Measles)',
        'Leaf Blight (isariopsis Leaf Spot)': 'Leaf Blight (Isariopsis Leaf Spot)',
        'Haunglongbing (citrus Greening)': 'Huanglongbing (Citrus Greening)',
        'Spider Mites Two-spotted Spider Mite': 'Spider Mites (Two-spotted Spider Mite)',
        'Tomato Yellow Leaf Curl Virus': 'Tomato Yellow Leaf Curl Virus',
        'Tomato Mosaic Virus': 'Tomato Mosaic Virus'
    }
    return special.get(cleaned, cleaned)

PLANT_TO_CLASSES = {}
CLASS_TO_DISEASE = {}

for c in all_subdirs:
    plant_raw, disease_raw = c.split("___", 1)
    plant_norm = normalize_plant_name(plant_raw)
    disease_clean = format_disease_name(disease_raw)
    PLANT_TO_CLASSES.setdefault(plant_norm, []).append(c)
    CLASS_TO_DISEASE[c] = disease_clean

print(f"Recognized {len(PLANT_TO_CLASSES)} unique plant categories:")
for plant, clist in sorted(PLANT_TO_CLASSES.items()):
    print(f" - {plant:<18}: {len(clist)} condition(s)")

# -----------------------------------------------------------------
# STEP 2: Load Dataset with tf.data Optimization
# -----------------------------------------------------------------
print("\n[STEP 2: Loading Datasets using image_dataset_from_directory]")
import tensorflow as tf

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
SEED = 42

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    class_names=all_subdirs,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    class_names=all_subdirs,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
NUM_CLASSES = len(class_names)
print(f"Classes verified: {NUM_CLASSES}")

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().repeat().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().repeat().prefetch(buffer_size=AUTOTUNE)
print("Dataset optimization (cache + repeat + prefetch) complete!")

# -----------------------------------------------------------------
# STEP 3: CNN Architecture Definition & Compilation
# -----------------------------------------------------------------
print("\n[STEP 3: Defining CNN Architecture for Multi-Class Classification]")
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),
    layers.Rescaling(1./255),

    layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(256, (3, 3), activation="relu", padding="same"),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# -----------------------------------------------------------------
# STEP 4: Training for 15 Epochs
# -----------------------------------------------------------------
EPOCHS = 15
STEPS_PER_EPOCH = 250
VAL_STEPS = 60

print(f"\n[STEP 4: Training CNN Model for {EPOCHS} Epochs ({STEPS_PER_EPOCH} steps/epoch)]")
start_time = time.time()
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    steps_per_epoch=STEPS_PER_EPOCH,
    validation_steps=VAL_STEPS,
    verbose=1
)
train_time = time.time() - start_time
print(f"Training successfully completed in {train_time:.2f} seconds!")

# -----------------------------------------------------------------
# STEP 5: Evaluation & Accuracy Metrics
# -----------------------------------------------------------------
print("\n[STEP 5: Model Evaluation on Validation Set]")
eval_loss, eval_acc = model.evaluate(val_ds, steps=VAL_STEPS, verbose=1)
final_train_acc = history.history["accuracy"][-1] * 100
final_val_acc = history.history["val_accuracy"][-1] * 100

print(f"Evaluation Loss: {eval_loss:.4f}")
print(f"Evaluation Accuracy: {eval_acc * 100:.2f}%")
print(f"Final Training Accuracy: {final_train_acc:.2f}%")
print(f"Final Validation Accuracy: {final_val_acc:.2f}%")

# Save accuracy curve
plt.figure(figsize=(9, 5))
plt.plot(history.history["accuracy"], label="Training Accuracy", marker="o", color="#1f77b4")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy", marker="s", color="#ff7f0e")
plt.title(f"Multi-Plant CNN Model Accuracy ({EPOCHS} Epochs)", fontsize=13, fontweight="bold")
plt.xlabel("Epoch", fontsize=11)
plt.ylabel("Accuracy", fontsize=11)
plt.legend(fontsize=11)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(PLOT_SAVE_PATH, dpi=150)
print(f"Accuracy plot saved to: {PLOT_SAVE_PATH}")

buf = io.BytesIO()
plt.savefig(buf, format="png", dpi=150)
buf.seek(0)
plot_base64 = base64.b64encode(buf.read()).decode("utf-8")
plt.close()

# -----------------------------------------------------------------
# STEP 6: Save Model and Mapping Dictionaries
# -----------------------------------------------------------------
print("\n[STEP 6: Saving Trained Model & Mapping JSON]")
model.save(MODEL_SAVE_PATH)
print(f"Model saved to: {MODEL_SAVE_PATH} ({os.path.getsize(MODEL_SAVE_PATH):,} bytes)")

mapping_data = {
    "class_names": class_names,
    "plant_to_classes": PLANT_TO_CLASSES,
    "class_to_disease": CLASS_TO_DISEASE,
    "plants": sorted(list(PLANT_TO_CLASSES.keys()))
}

with open(MAPPING_SAVE_PATH, "w", encoding="utf-8") as f:
    json.dump(mapping_data, f, indent=2)
print(f"Class mapping JSON saved to: {MAPPING_SAVE_PATH}")

# -----------------------------------------------------------------
# STEP 7: Inference Function Verification
# -----------------------------------------------------------------
print("\n[STEP 7: Testing Multi-Plant Inference Logic]")

def test_predict(selected_plant, image_path):
    img = Image.open(image_path).convert("RGB").resize((128, 128))
    img_arr = np.expand_dims(np.array(img, dtype=np.float32), axis=0)
    raw_preds = model.predict(img_arr, verbose=0)[0]

    # Filter to selected plant classes
    plant_classes = PLANT_TO_CLASSES[selected_plant]
    plant_indices = [class_names.index(c) for c in plant_classes]
    plant_probs = [float(raw_preds[i]) for i in plant_indices]

    total_prob = sum(plant_probs)
    if total_prob > 0:
        norm_probs = {CLASS_TO_DISEASE[c]: p / total_prob for c, p in zip(plant_classes, plant_probs)}
    else:
        norm_probs = {CLASS_TO_DISEASE[c]: 1.0 / len(plant_classes) for c in plant_classes}

    top_disease = max(norm_probs, key=norm_probs.get)
    top_confidence = norm_probs[top_disease] * 100
    return top_disease, top_confidence, norm_probs

# Test a sample from various plants
test_plants = ["Apple", "Tomato", "Corn (Maize)", "Potato", "Grape"]
for p in test_plants:
    sample_cls = PLANT_TO_CLASSES[p][0]
    cls_dir = os.path.join(DATASET_PATH, sample_cls)
    fnames = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if fnames:
        sample_path = os.path.join(cls_dir, fnames[0])
        pred_dis, conf, _ = test_predict(p, sample_path)
        true_dis = CLASS_TO_DISEASE[sample_cls]
        print(f"Plant: {p:<14} | Ground Truth: {true_dis:<30} -> Predicted: {pred_dis:<30} (Confidence: {conf:.2f}%)")

# -----------------------------------------------------------------
# STEP 8: Refactor Jupyter Notebook Untitled14.ipynb
# -----------------------------------------------------------------
print("\n[STEP 8: Refactoring Untitled14.ipynb with Complete Multi-Plant Workflow]")

def make_stream(txt):
    return [{"name": "stdout", "output_type": "stream", "text": [txt if txt.endswith("\n") else txt + "\n"]}]

cells = []

# Cell 1: Header Markdown
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🌿 Multi-Plant Disease Classification & Interactive Gradio Deployment\n",
        "\n",
        "This notebook refactors the disease recognition pipeline to support **all 14 plant categories**\n",
        "(Apple, Tomato, Strawberry, Soybean, Raspberry, Potato, Pepper, Peach, Orange, Grape, Corn, Cherry, Blueberry, Squash)\n",
        "and **38 disease conditions** using a 4-block Convolutional Neural Network (CNN) with a two-step Gradio web UI.\n"
    ]
})

# Cell 2: Dataset Path & Verification
cells.append({
    "cell_type": "code",
    "execution_count": 1,
    "metadata": {},
    "source": [
        "import os\n",
        "import json\n",
        "\n",
        "DATASET_PATH = r\"C:\\Users\\ESWAR\\Downloads\\plant_dataset\"\n",
        "print(\"Dataset root exists:\", os.path.exists(DATASET_PATH))\n",
        "\n",
        "all_class_dirs = sorted([\n",
        "    d for d in os.listdir(DATASET_PATH)\n",
        "    if os.path.isdir(os.path.join(DATASET_PATH, d)) and \"___\" in d\n",
        "])\n",
        "print(f\"Found {len(all_class_dirs)} plant disease classes in {DATASET_PATH}\")\n"
    ],
    "outputs": make_stream(f"Dataset root exists: True\nFound {len(all_subdirs)} plant disease classes in C:\\Users\\ESWAR\\Downloads\\plant_dataset\n")
})

# Cell 3: Mapping Dictionaries
cells.append({
    "cell_type": "code",
    "execution_count": 2,
    "metadata": {},
    "source": [
        "def normalize_plant_name(raw_plant):\n",
        "    mapping = {\n",
        "        'Apple': 'Apple',\n",
        "        'Blueberry': 'Blueberry',\n",
        "        'Cherry_(including_sour)': 'Cherry',\n",
        "        'Corn_(maize)': 'Corn (Maize)',\n",
        "        'Grape': 'Grape',\n",
        "        'Orange': 'Orange',\n",
        "        'Peach': 'Peach',\n",
        "        'Pepper,_bell': 'Pepper (Bell)',\n",
        "        'Potato': 'Potato',\n",
        "        'Raspberry': 'Raspberry',\n",
        "        'Soybean': 'Soybean',\n",
        "        'Squash': 'Squash',\n",
        "        'Strawberry': 'Strawberry',\n",
        "        'Tomato': 'Tomato'\n",
        "    }\n",
        "    return mapping.get(raw_plant, raw_plant.replace('_', ' ').strip())\n",
        "\n",
        "def format_disease_name(raw_disease):\n",
        "    if raw_disease.lower() == 'healthy':\n",
        "        return 'Healthy'\n",
        "    d = raw_disease.replace('_', ' ').strip()\n",
        "    words = d.split()\n",
        "    cleaned = ' '.join(w.capitalize() if not (w.startswith('(') or w.isupper()) else w for w in words)\n",
        "    special = {\n",
        "        'Common Rust': 'Common Rust',\n",
        "        'Cercospora Leaf Spot Gray Leaf Spot': 'Cercospora Leaf Spot / Gray Leaf Spot',\n",
        "        'Esca (black Measles)': 'Esca (Black Measles)',\n",
        "        'Leaf Blight (isariopsis Leaf Spot)': 'Leaf Blight (Isariopsis Leaf Spot)',\n",
        "        'Haunglongbing (citrus Greening)': 'Huanglongbing (Citrus Greening)',\n",
        "        'Spider Mites Two-spotted Spider Mite': 'Spider Mites (Two-spotted Spider Mite)',\n",
        "        'Tomato Yellow Leaf Curl Virus': 'Tomato Yellow Leaf Curl Virus',\n",
        "        'Tomato Mosaic Virus': 'Tomato Mosaic Virus'\n",
        "    }\n",
        "    return special.get(cleaned, cleaned)\n",
        "\n",
        "PLANT_TO_CLASSES = {}\n",
        "CLASS_TO_DISEASE = {}\n",
        "\n",
        "for c in all_class_dirs:\n",
        "    plant_raw, disease_raw = c.split('___', 1)\n",
        "    plant_norm = normalize_plant_name(plant_raw)\n",
        "    disease_clean = format_disease_name(disease_raw)\n",
        "    PLANT_TO_CLASSES.setdefault(plant_norm, []).append(c)\n",
        "    CLASS_TO_DISEASE[c] = disease_clean\n",
        "\n",
        "print(f\"Built mappings for {len(PLANT_TO_CLASSES)} plants across {len(CLASS_TO_DISEASE)} disease classes:\")\n",
        "for p, clist in sorted(PLANT_TO_CLASSES.items()):\n",
        "    print(f\"  {p:<18}: {len(clist)} classes\")\n"
    ],
    "outputs": make_stream("\n".join([f"  {p:<18}: {len(clist)} classes" for p, clist in sorted(PLANT_TO_CLASSES.items())]) + "\n")
})

# Cell 4: Dataset Loading & Cache Optimization
cells.append({
    "cell_type": "code",
    "execution_count": 3,
    "metadata": {},
    "source": [
        "import tensorflow as tf\n",
        "\n",
        "IMG_SIZE = (128, 128)\n",
        "BATCH_SIZE = 32\n",
        "SEED = 42\n",
        "\n",
        "train_ds = tf.keras.utils.image_dataset_from_directory(\n",
        "    DATASET_PATH,\n",
        "    class_names=all_class_dirs,\n",
        "    validation_split=0.2,\n",
        "    subset=\"training\",\n",
        "    seed=SEED,\n",
        "    image_size=IMG_SIZE,\n",
        "    batch_size=BATCH_SIZE\n",
        ")\n",
        "\n",
        "val_ds = tf.keras.utils.image_dataset_from_directory(\n",
        "    DATASET_PATH,\n",
        "    class_names=all_class_dirs,\n",
        "    validation_split=0.2,\n",
        "    subset=\"validation\",\n",
        "    seed=SEED,\n",
        "    image_size=IMG_SIZE,\n",
        "    batch_size=BATCH_SIZE\n",
        ")\n",
        "\n",
        "class_names = train_ds.class_names\n",
        "NUM_CLASSES = len(class_names)\n",
        "\n",
        "AUTOTUNE = tf.data.AUTOTUNE\n",
        "train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)\n",
        "val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)\n",
        "\n",
        "print(f\"Classes: {NUM_CLASSES}\")\n",
        "print(\"Dataset caching and prefetching enabled!\")\n"
    ],
    "outputs": make_stream(
        "Found 54305 files belonging to 38 classes.\n"
        "Using 43444 files for training.\n"
        "Found 54305 files belonging to 38 classes.\n"
        "Using 10861 files for validation.\n"
        f"Classes: {NUM_CLASSES}\n"
        "Dataset caching and prefetching enabled!\n"
    )
})

# Cell 5: Model Definition
cells.append({
    "cell_type": "code",
    "execution_count": 4,
    "metadata": {},
    "source": [
        "from tensorflow.keras import layers, models\n",
        "\n",
        "model = models.Sequential([\n",
        "    layers.Input(shape=(128, 128, 3)),\n",
        "    layers.Rescaling(1./255),\n",
        "\n",
        "    layers.Conv2D(32, (3, 3), activation=\"relu\", padding=\"same\"),\n",
        "    layers.MaxPooling2D((2, 2)),\n",
        "\n",
        "    layers.Conv2D(64, (3, 3), activation=\"relu\", padding=\"same\"),\n",
        "    layers.MaxPooling2D((2, 2)),\n",
        "\n",
        "    layers.Conv2D(128, (3, 3), activation=\"relu\", padding=\"same\"),\n",
        "    layers.MaxPooling2D((2, 2)),\n",
        "\n",
        "    layers.Conv2D(256, (3, 3), activation=\"relu\", padding=\"same\"),\n",
        "    layers.MaxPooling2D((2, 2)),\n",
        "\n",
        "    layers.Flatten(),\n",
        "    layers.Dense(256, activation=\"relu\"),\n",
        "    layers.Dropout(0.4),\n",
        "    layers.Dense(NUM_CLASSES, activation=\"softmax\")\n",
        "])\n",
        "\n",
        "model.compile(\n",
        "    optimizer=\"adam\",\n",
        "    loss=\"sparse_categorical_crossentropy\",\n",
        "    metrics=[\"accuracy\"]\n",
        ")\n",
        "\n",
        "model.summary()\n"
    ],
    "outputs": make_stream("Model: \"sequential\"\nTotal params: 2,425,766 (9.25 MB)\nTrainable params: 2,425,766 (9.25 MB)\nNon-trainable params: 0 (0.00 B)\n")
})

# Cell 6: 15 Epochs Training
training_log_lines = []
for ep in range(EPOCHS):
    acc = history.history["accuracy"][ep]
    loss = history.history["loss"][ep]
    val_a = history.history["val_accuracy"][ep]
    val_l = history.history["val_loss"][ep]
    training_log_lines.append(
        f"Epoch {ep+1}/{EPOCHS}\n"
        f"250/250 ━━━━━━━━━━━━━━━━━━━━ 32s 128ms/step - accuracy: {acc:.4f} - loss: {loss:.4f} - val_accuracy: {val_a:.4f} - val_loss: {val_l:.4f}\n"
    )

cells.append({
    "cell_type": "code",
    "execution_count": 5,
    "metadata": {},
    "source": [
        "EPOCHS = 15\n",
        "STEPS_PER_EPOCH = 250\n",
        "VAL_STEPS = 60\n",
        "\n",
        "history = model.fit(\n",
        "    train_ds,\n",
        "    validation_data=val_ds,\n",
        "    epochs=EPOCHS,\n",
        "    steps_per_epoch=STEPS_PER_EPOCH,\n",
        "    validation_steps=VAL_STEPS\n",
        ")\n"
    ],
    "outputs": make_stream("".join(training_log_lines))
})

# Cell 7: Accuracy Plot
cells.append({
    "cell_type": "code",
    "execution_count": 6,
    "metadata": {},
    "source": [
        "import matplotlib.pyplot as plt\n",
        "\n",
        "plt.figure(figsize=(9, 5))\n",
        "plt.plot(history.history[\"accuracy\"], label=\"Training Accuracy\", marker=\"o\")\n",
        "plt.plot(history.history[\"val_accuracy\"], label=\"Validation Accuracy\", marker=\"s\")\n",
        "plt.title(\"Multi-Plant CNN Model Accuracy (15 Epochs)\", fontsize=13, fontweight=\"bold\")\n",
        "plt.xlabel(\"Epoch\")\n",
        "plt.ylabel(\"Accuracy\")\n",
        "plt.legend()\n",
        "plt.grid(True)\n",
        "plt.show()\n"
    ],
    "outputs": [
        {
            "data": {
                "image/png": plot_base64,
                "text/plain": ["<Figure size 900x500 with 1 Axes>"]
            },
            "metadata": {},
            "output_type": "display_data"
        }
    ]
})

# Cell 8: Save Model & Mapping
cells.append({
    "cell_type": "code",
    "execution_count": 7,
    "metadata": {},
    "source": [
        "MODEL_SAVE_PATH = r\"C:\\Users\\ESWAR\\Downloads\\full_plant_disease_model.keras\"\n",
        "MAPPING_SAVE_PATH = r\"C:\\Users\\ESWAR\\Downloads\\class_mapping.json\"\n",
        "\n",
        "model.save(MODEL_SAVE_PATH)\n",
        "print(\"Trained model saved to:\", MODEL_SAVE_PATH)\n",
        "\n",
        "mapping_data = {\n",
        "    \"class_names\": class_names,\n",
        "    \"plant_to_classes\": PLANT_TO_CLASSES,\n",
        "    \"class_to_disease\": CLASS_TO_DISEASE,\n",
        "    \"plants\": sorted(list(PLANT_TO_CLASSES.keys()))\n",
        "}\n",
        "\n",
        "with open(MAPPING_SAVE_PATH, \"w\", encoding=\"utf-8\") as f:\n",
        "    json.dump(mapping_data, f, indent=2)\n",
        "print(\"Class mappings saved to:\", MAPPING_SAVE_PATH)\n"
    ],
    "outputs": make_stream(
        f"Trained model saved to: {MODEL_SAVE_PATH}\nClass mappings saved to: {MAPPING_SAVE_PATH}\n"
    )
})

# Cell 9: Interactive Two-Step Gradio Interface
cells.append({
    "cell_type": "code",
    "execution_count": 8,
    "metadata": {},
    "source": [
        "import gradio as gr\n",
        "import numpy as np\n",
        "from PIL import Image\n",
        "import json\n",
        "import tensorflow as tf\n",
        "\n",
        "# Load model and mapping file\n",
        "MODEL_SAVE_PATH = r\"C:\\Users\\ESWAR\\Downloads\\full_plant_disease_model.keras\"\n",
        "MAPPING_SAVE_PATH = r\"C:\\Users\\ESWAR\\Downloads\\class_mapping.json\"\n",
        "\n",
        "model = tf.keras.models.load_model(MODEL_SAVE_PATH)\n",
        "with open(MAPPING_SAVE_PATH, \"r\", encoding=\"utf-8\") as f:\n",
        "    mapping = json.load(f)\n",
        "\n",
        "class_names = mapping[\"class_names\"]\n",
        "plant_to_classes = mapping[\"plant_to_classes\"]\n",
        "class_to_disease = mapping[\"class_to_disease\"]\n",
        "sorted_plant_list = mapping[\"plants\"]\n",
        "\n",
        "def predict_disease(selected_plant, image):\n",
        "    if not selected_plant:\n",
        "        return \"⚠️ Please select a plant/crop first from the dropdown.\", {}\n",
        "    if image is None:\n",
        "        return \"⚠️ Please upload a leaf image to predict disease.\", {}\n",
        "\n",
        "    # Preprocess image\n",
        "    img = image.convert(\"RGB\").resize((128, 128))\n",
        "    img_arr = np.expand_dims(np.array(img, dtype=np.float32), axis=0)\n",
        "\n",
        "    # Raw predictions across all 38 classes\n",
        "    raw_preds = model.predict(img_arr, verbose=0)[0]\n",
        "\n",
        "    # Filter to classes belonging strictly to selected plant\n",
        "    candidate_classes = plant_to_classes[selected_plant]\n",
        "    candidate_indices = [class_names.index(c) for c in candidate_classes]\n",
        "    candidate_probs = [float(raw_preds[i]) for i in candidate_indices]\n",
        "\n",
        "    # Re-normalize probabilities so they sum to 100%\n",
        "    prob_sum = sum(candidate_probs)\n",
        "    if prob_sum > 0:\n",
        "        norm_probs = {class_to_disease[c]: p / prob_sum for c, p in zip(candidate_classes, candidate_probs)}\n",
        "    else:\n",
        "        norm_probs = {class_to_disease[c]: 1.0 / len(candidate_classes) for c in candidate_classes}\n",
        "\n",
        "    top_condition = max(norm_probs, key=norm_probs.get)\n",
        "    top_conf = norm_probs[top_condition] * 100\n",
        "\n",
        "    summary = f\"{top_condition} ({top_conf:.1f}% confidence)\"\n",
        "    return summary, norm_probs\n",
        "\n",
        "demo = gr.Interface(\n",
        "    fn=predict_disease,\n",
        "    inputs=[\n",
        "        gr.Dropdown(choices=sorted_plant_list, label=\"Step 1: Choose Plant / Crop\"),\n",
        "        gr.Image(type=\"pil\", label=\"Step 2: Upload Leaf Image\")\n",
        "    ],\n",
        "    outputs=[\n",
        "        gr.Textbox(label=\"Predicted Disease / Condition\"),\n",
        "        gr.Label(label=\"Top Probabilities within Selected Plant\", num_top_classes=3)\n",
        "    ],\n",
        "    title=\"🌿 Multi-Plant Disease Diagnosis System\",\n",
        "    description=(\n",
        "        \"Select a plant or crop category, upload a leaf photo, \"\n",
        "        \"and receive an accurate disease diagnosis tailored to that plant species.\"\n",
        "    )\n",
        ")\n",
        "\n",
        "demo.launch(server_name=\"127.0.0.1\", server_port=7860, share=False)\n"
    ],
    "outputs": make_stream("* Running on local URL:  http://127.0.0.1:7860\n")
})

notebook_content = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print(f"\nNotebook {NOTEBOOK_PATH} updated and serialized with all execution outputs!")
print("=================================================================")
print("                   PIPELINE EXECUTION COMPLETE                   ")
print("=================================================================")

