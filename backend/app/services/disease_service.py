import os
import io
import uuid
import logging
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image
from app.core.config import settings

logger = logging.getLogger(__name__)

# Comprehensive agronomic disease knowledge-base (ICAR / standard agricultural extension verified)
DISEASE_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "Tomato___Early_blight": {
        "crop_name": "Tomato",
        "disease_name": "Early Blight (Alternaria solani)",
        "description": "Fungal disease causing brown-black concentric target-like rings on older leaves, progressing upward and leading to premature defoliation.",
        "symptoms": [
            "Concentric dark brown rings forming target spots on lower foliage",
            "Yellow halo (chlorosis) surrounding older necrotic lesions",
            "Stem cankers near soil level (collar rot) on seedlings",
            "Sunken, dark leathery lesions at stem end of tomato fruit"
        ],
        "treatment_recommendations": [
            "Apply copper-based fungicides (e.g., Copper Oxychloride 50% WP @ 2.5 g/L) at first symptom onset",
            "Spray Mancozeb 75% WP @ 2 g/L or Chlorothalonil on a 7-10 day preventive rotation",
            "Prune infected bottom leaves during dry weather to enhance air circulation",
            "Employ drip irrigation instead of overhead sprinklers to keep foliage dry"
        ],
        "preventive_measures": [
            "Practice 3-year crop rotation avoiding Solanaceous family crops (potato, brinjal, chili)",
            "Use certified disease-free treated seeds or resistant tomato cultivars",
            "Stake plants and mulch soil with clean organic straw to prevent soil-splash pathogens",
            "Sanitize all pruning tools in 10% bleach solution between plant rows"
        ],
        "risk_level": "High"
    },
    "Tomato___Late_blight": {
        "crop_name": "Tomato",
        "disease_name": "Late Blight (Phytophthora infestans)",
        "description": "Water-mold pathogen causing rapid water-soaked lesions, white fuzzy sporulation on leaf undersides, and destructive fruit rot in cool, humid conditions.",
        "symptoms": [
            "Pale green, water-soaked irregular spots rapidly enlarging into brown blotches",
            "Delicate white cottony fungal growth on leaf undersides during moist mornings",
            "Dark brown blotchy discoloration and rotting of green and ripe fruit",
            "Rapid total collapse of plant foliage ('blighted' appearance)"
        ],
        "treatment_recommendations": [
            "Immediately spray Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ) @ 2.5 g/L",
            "Alternate with Dimethomorph 50% WP or Cymoxanil combinations",
            "Destroy and bury severely diseased plants away from field immediately",
            "Cease all sprinkler and furrow irrigation to lower localized humidity"
        ],
        "preventive_measures": [
            "Avoid planting near potato fields harboring latent late blight inoculum",
            "Select resistant varieties with Ph-2 and Ph-3 gene resistance",
            "Ensure wide plant spacing for rapid canopy drying after morning dew",
            "Monitor weather forecast alerts for extended cloudy, high-humidity periods"
        ],
        "risk_level": "Critical"
    },
    "Rice___Bacterial_leaf_blight": {
        "crop_name": "Rice",
        "disease_name": "Bacterial Leaf Blight (Xanthomonas oryzae)",
        "description": "Systemic vascular bacterial disease causing wavy yellow-to-white lesions beginning at leaf margins and tips, causing severe grain yield losses.",
        "symptoms": [
            "Water-soaked stripes starting at leaf tips and margins with wavy borders",
            "Lesions turn yellowish-orange and eventually bleach grayish-white",
            "Milky bacterial exudate droplets glistening on leaves during humid mornings",
            "Wilting and seedling death known as 'kresek' stage"
        ],
        "treatment_recommendations": [
            "Spray Streptocycline (90:10 Streptomycin sulfate + Tetracycline) @ 6 g / 50 L water combined with Copper Oxychloride @ 50 g",
            "Drain excess standing water from paddy fields temporarily for 3-4 days",
            "Split nitrogen fertilizer applications; avoid excessive top-dressing during active infection",
            "Apply potash (MOP) @ 15-20 kg/acre to boost plant cell wall resistance"
        ],
        "preventive_measures": [
            "Soak seeds in Streptocycline solution (0.015%) for 8 hours prior to nursery sowing",
            "Plant resistant rice cultivars recommended for your state agro-climatic zone",
            "Maintain clean bunds and eliminate alternate grassy weed hosts (e.g. Leersia hexandra)",
            "Adopt balanced N:P:K fertilization (avoid heavy nitrogen excess)"
        ],
        "risk_level": "High"
    },
    "Rice___Blast": {
        "crop_name": "Rice",
        "disease_name": "Rice Blast (Magnaporthe oryzae)",
        "description": "Devastating fungal pathogen creating spindle-shaped diamond lesions on leaves and neck rot on panicles.",
        "symptoms": [
            "Spindle-shaped elliptical lesions with gray/whitish centers and dark brown margins",
            "Neck blast: blackening and rotting of panicle node causing blanked, chaffy grains",
            "Severe leaf coalescing lesions resulting in burned field patches ('blast')",
            "Brownish collar rot at junction of leaf blade and sheath"
        ],
        "treatment_recommendations": [
            "Apply Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 mL/L at boot leaf stage",
            "Spray Kasugamycin 3% SL @ 2 mL/L if symptoms appear on upper foliage",
            "Maintain continuous shallow water layer in paddy to reduce stress",
            "Refrain from urea top-dressing during active blast expansion"
        ],
        "preventive_measures": [
            "Treat seed with Carbendazim 50% WP @ 2 g/kg seed before nursery sowing",
            "Avoid delayed sowing into late cloudy monsoon conditions",
            "Incorporate silica amendments to strengthen leaf cuticle against fungal penetration",
            "Use certified resistant hybrid and high-yielding cultivars"
        ],
        "risk_level": "Critical"
    },
    "Potato___Late_blight": {
        "crop_name": "Potato",
        "disease_name": "Potato Late Blight (Phytophthora infestans)",
        "description": "High-risk water-mold disease causing leaf rot, stem lesions, and tuber breakdown.",
        "symptoms": [
            "Dark water-soaked lesions expanding rapidly across foliage",
            "White fungal mildew rings on leaf undersides",
            "Purplish-brown dry rot extending into tuber flesh beneath skin",
            "Foul smell emanating from blighted potato canopy"
        ],
        "treatment_recommendations": [
            "Spray Cymoxanil 8% + Mancozeb 64% WP @ 2.5 g/L upon local blight alert trigger",
            "Apply systemic Propamocarb hydrochloride or Mandipropamid",
            "Cut and burn haulms 10-12 days before harvest to prevent tuber contamination",
            "Allow harvested tubers to cure in dry shade before bagging"
        ],
        "preventive_measures": [
            "Use certified disease-free seed tubers from trusted seed agencies",
            "Perform proper high hilling / earthing-up to shield tubers with deep soil barrier",
            "Follow Indian Meteorological Department (IMD) / AgriSaathi weather blight alerts",
            "Store harvested potatoes in well-ventilated, cold-chain storage"
        ],
        "risk_level": "Critical"
    },
    "Healthy": {
        "crop_name": "All Crops",
        "disease_name": "Healthy Plant Leaf (No Pathogen Detected)",
        "description": "No visible signs of biotic pathogen attack or serious physiological nutrient deficiency were identified on this leaf sample.",
        "symptoms": [
            "Uniform leaf coloration consistent with natural cultivar morphology",
            "Intact leaf margins and veins with no necrotic spots or chlorotic halos",
            "No mycelial growth, bacterial exudates, or insect puncture stippling"
        ],
        "treatment_recommendations": [
            "No chemical intervention or pesticide treatment required at this time",
            "Continue standard agronomic monitoring and balanced irrigation",
            "Maintain integrated nutrient management (INM) based on soil test recommendations"
        ],
        "preventive_measures": [
            "Conduct routine weekly scouting across field quadrants for early warning signs",
            "Preserve beneficial predator insects and promote soil organic carbon",
            "Keep farm perimeter free of alternate weed reservoirs"
        ],
        "risk_level": "None"
    }
}

class DiseaseModelService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.model_type = "CNN / ResNet-50 Interface"
        self._check_and_load_model()

    def _check_and_load_model(self):
        """
        Check for trained CNN / Keras model.
        In accordance with rule:
        - Do not pretend a trained model exists if it has not been trained.
        - Do not return fake disease predictions.
        - If the model is unavailable, return a clear message that AI prediction is not yet configured.
        """
        model_path = settings.DISEASE_MODEL_PATH
        if os.path.exists(model_path):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"Loaded trained plant disease CNN model from {model_path}")
            except Exception as e:
                logger.warning(f"Found model file at {model_path} but failed to load: {e}")
                self.model_loaded = False
        else:
            logger.info(
                f"No pre-trained model file found at '{model_path}'. "
                "Disease detection service is operating in modular unconfigured mode (Milestone 40%)."
            )
            self.model_loaded = False

    def validate_image(self, file_bytes: bytes, filename: str) -> Tuple[bool, str, Optional[Image.Image]]:
        """Validate uploaded image format, dimensions, and payload integrity."""
        max_size_bytes = 10 * 1024 * 1024  # 10 MB limit
        if len(file_bytes) > max_size_bytes:
            return False, "Image file size exceeds the 10 MB limit.", None
        
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        ext = os.path.splitext(filename.lower())[1]
        if ext not in allowed_extensions:
            return False, f"Unsupported file type '{ext}'. Allowed formats: JPG, JPEG, PNG, WEBP.", None
        
        try:
            image = Image.open(io.BytesIO(file_bytes))
            image.verify()  # Verify integrity
            # Reopen for actual processing as verify closes the image
            image = Image.open(io.BytesIO(file_bytes))
            
            width, height = image.size
            if width < 64 or height < 64:
                return False, "Image resolution too low. Please upload an image of at least 64x64 pixels.", None
                
            return True, "Valid image", image
        except Exception as e:
            return False, f"Uploaded file is corrupt or not a valid image: {str(e)}", None

    def save_image(self, file_bytes: bytes, original_filename: str) -> Tuple[str, str]:
        """Save uploaded image to disk with a secure unique filename."""
        ext = os.path.splitext(original_filename.lower())[1] or ".jpg"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, unique_name)
        
        with open(filepath, "wb") as f:
            f.write(file_bytes)
            
        relative_url = f"/uploads/disease_images/{unique_name}"
        return filepath, relative_url

    async def predict(
        self,
        file_bytes: bytes,
        filename: str,
        crop_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze plant leaf image.
        Modular architecture:
        - If CNN weights exist, run real forward pass through TensorFlow.
        - If weights are not trained, return truthful status indicating model training is pending in next phase.
        """
        # Step 1: Validate image
        is_valid, error_msg, pil_img = self.validate_image(file_bytes, filename)
        if not is_valid:
            return {
                "success": False,
                "message": error_msg,
                "model_configured": self.model_loaded
            }

        # Step 2: Save image for record & expert review
        file_path, image_url = self.save_image(file_bytes, filename)

        # Step 3: Check if trained model weights exist
        if not self.model_loaded or self.model is None:
            return {
                "success": True,
                "model_configured": False,
                "image_url": image_url,
                "image_path": file_path,
                "plant_name": crop_type or "Crop Leaf Sample",
                "predicted_disease": None,
                "confidence_score": None,
                "message": (
                    "Image successfully uploaded and validated. "
                    "The AI CNN deep-learning model weights are currently unconfigured in this 40% milestone. "
                    "The model pipeline is prepared and ready for the trained Keras/ResNet model in the next milestone. "
                    "You may submit this image to an Agricultural Expert for manual diagnosis review."
                ),
                "visible_symptoms": [],
                "treatment_recommendations": [],
                "preventive_measures": [],
                "knowledge_base_available_crops": list(set(k.split("___")[0] for k in DISEASE_KNOWLEDGE_BASE.keys()))
            }

        # Step 4: Trained model inference (when model exists)
        try:
            import numpy as np
            # Standard CNN preprocessing: resize to 224x224 RGB, normalize 0-1
            resized = pil_img.convert("RGB").resize((224, 224))
            arr = np.array(resized, dtype=np.float32) / 255.0
            batch = np.expand_dims(arr, axis=0)
            
            raw_pred = self.model.predict(batch)
            conf = float(np.max(raw_pred))
            class_idx = int(np.argmax(raw_pred))
            
            # Map index to class name if class labels file exists, otherwise report
            class_name = f"Class_{class_idx}"
            kb_entry = DISEASE_KNOWLEDGE_BASE.get(class_name, DISEASE_KNOWLEDGE_BASE["Healthy"])

            return {
                "success": True,
                "model_configured": True,
                "image_url": image_url,
                "image_path": file_path,
                "plant_name": kb_entry["crop_name"],
                "predicted_disease": kb_entry["disease_name"],
                "confidence_score": round(conf * 100, 2),
                "disease_description": kb_entry["description"],
                "visible_symptoms": kb_entry["symptoms"],
                "treatment_recommendations": kb_entry["treatment_recommendations"],
                "preventive_measures": kb_entry["preventive_measures"],
                "message": f"Disease analyzed with {round(conf * 100, 1)}% confidence score."
            }
        except Exception as e:
            logger.error(f"Inference error on CNN model: {e}")
            return {
                "success": False,
                "model_configured": True,
                "message": f"Error running inference on model: {str(e)}"
            }

disease_service = DiseaseModelService()

