import json
import torch
import torch.nn as nn
from torchvision import models
from pathlib import Path
from typing import Dict, Any, Tuple
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("DiseaseDetector")

class DiseaseDetector:
    def __init__(self):
        self.model_path = settings.DISEASE_MODEL_PATH
        self.model = None
        self.labels = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()
        
    def _load_model(self):
        """Attempts to load the .pth model, warns if not present."""
        
        # Ensure knowledge base exists for mapping
        kb_path = settings.BASE_DIR / 'knowledge' / 'diseases.json'
        if kb_path.exists():
            with open(kb_path, 'r') as f:
                data = json.load(f)
                # Map array index (0, 1, 2) to the disease object
                self.labels = {str(item['id']): item for item in data}

        if self.model_path.exists():
            try:
                logger.info(f"Loading PyTorch model from {self.model_path}")
                # Initialize MobileNetV2 with 3 classes
                self.model = models.mobilenet_v2(weights=None)
                num_ftrs = self.model.classifier[1].in_features
                
                # Number of classes is based on diseases.json length, or default 3
                num_classes = len(self.labels) if self.labels else 3
                
                self.model.classifier[1] = nn.Linear(num_ftrs, num_classes)
                self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                self.model = self.model.to(self.device)
                self.model.eval()
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.model = None
        else:
            logger.warning(f"Model weights missing at {self.model_path}. Using fallback logic.")
                
    def predict(self, tensor_or_none) -> Tuple[Dict[str, Any], float]:
        """Runs inference. Mocks if model unavailable."""
        if self.model is None or tensor_or_none is None:
            logger.warning("Mocking diagnosis due to missing model or tensor.")
            # Fallback mock diagnosis (just returns first item in labels)
            if self.labels:
                mock_res = list(self.labels.values())[0]
            else:
                mock_res = {"name": "Unknown Disease", "cause": "N/A", "solution": ["N/A"]}
            return mock_res, 0.65
            
        try:
            tensor = tensor_or_none.to(self.device)
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                confidence, pred_idx = torch.max(probabilities, 0)
                
                idx_str = str(pred_idx.item())
                if idx_str in self.labels:
                    disease_info = self.labels[idx_str]
                else:
                    disease_info = {"name": f"Unknown Class {idx_str}", "cause": "Unknown", "solution": []}
                    
                return disease_info, confidence.item()
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            mock_res = list(self.labels.values())[0] if self.labels else {"name": "Error", "cause": "N/A", "solution": ["N/A"]}
            return mock_res, 0.0

