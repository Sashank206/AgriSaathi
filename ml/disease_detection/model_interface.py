"""
AgriSaathi - Plant Disease Detection Model Interface
Modular CNN architecture ready for TensorFlow/Keras / ResNet-50 weights.
"""
import os
import json
import logging
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)

class PlantDiseaseCNNModel:
    def __init__(self, weights_path: str = "ml/saved_models/plant_disease_model.h5"):
        self.weights_path = weights_path
        self.model = None
        self.input_shape = (224, 224, 3)
        self.classes = []
        self._load_classes()

    def _load_classes(self):
        labels_file = os.path.join(os.path.dirname(__file__), "labels.json")
        if os.path.exists(labels_file):
            try:
                with open(labels_file, "r") as f:
                    self.classes = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load labels: {e}")

    def load_weights(self) -> bool:
        if not os.path.exists(self.weights_path):
            return False
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(self.weights_path)
            return True
        except Exception as e:
            logger.error(f"Failed loading weights from {self.weights_path}: {e}")
            return False

