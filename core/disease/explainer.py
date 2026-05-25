try:
    from pytorch_grad_cam import GradCAM
    from pytorch_grad_cam.utils.image import show_cam_on_image
    import torch
except ImportError:
    GradCAM = None
    show_cam_on_image = None
    torch = None

import numpy as np
from PIL import Image
from utils.logger import get_logger

logger = get_logger("DiseaseExplainer")

class DiseaseExplainer:
    def __init__(self, model):
        self.model = model
        
    def generate_heatmap(self, input_tensor, original_img: Image.Image) -> 'Image.Image':
        """
        Generates a Grad-CAM heatmap overlay for the given inference tensor.
        Returns the original image if model/library is missing.
        """
        if not GradCAM or not torch or self.model is None or input_tensor is None:
            logger.warning("Grad-CAM, PyTorch, or Model missing. Returning raw image.")
            return original_img
            
        try:
            # For a typical ResNet/CNN, target the last convolutional layer
            target_layers = [self.model.layer4[-1]] if hasattr(self.model, 'layer4') else []
            if not target_layers:
                logger.warning("Could not automatically determine target layers. Returning raw image.")
                return original_img
                
            cam = GradCAM(model=self.model, target_layers=target_layers, use_cuda=torch.cuda.is_available())
            
            # Generate CAM (Grayscale)
            grayscale_cam = cam(input_tensor=input_tensor, targets=None)[0, :]
            
            # Normalize original image to [0,1]
            img_np = np.array(original_img).astype(np.float32) / 255.0
            
            # Overlay
            cam_image = show_cam_on_image(img_np, grayscale_cam, use_rgb=True)
            return Image.fromarray(cam_image)
            
        except Exception as e:
            logger.error(f"Failed to generate Grad-CAM heatmap: {e}")
            return original_img
