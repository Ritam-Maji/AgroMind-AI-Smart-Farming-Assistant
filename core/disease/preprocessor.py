try:
    import torch
    from torchvision import transforms
except ImportError:
    torch = None
    transforms = None

from PIL import Image
from utils.logger import get_logger

logger = get_logger("DiseasePreprocessor")

class DiseasePreprocessor:
    @staticmethod
    def preprocess_image(image: Image.Image) -> 'torch.Tensor':
        """
        Normalizes a PIL image for PyTorch CNN inference.
        Returns a mock tensor if torchvision is not installed.
        """
        if not transforms or not torch:
            logger.warning("torch/torchvision not available. Returning a dummy tensor.")
            return None
            
        transform_pipeline = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])
        
        try:
            tensor = transform_pipeline(image)
            # Add batch dimension
            return tensor.unsqueeze(0)
        except Exception as e:
            logger.error(f"Failed to preprocess image: {e}")
            raise
