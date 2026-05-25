import io
from typing import Union
from pathlib import Path
from PIL import Image

def load_image(source: Union[str, Path, bytes, io.BytesIO]) -> Image.Image:
    """
    Loads an image from a path, raw bytes, or file-like object and standardizes it to RGB.
    """
    try:
        if isinstance(source, (str, Path)):
            img = Image.open(source)
        elif isinstance(source, bytes):
            img = Image.open(io.BytesIO(source))
        elif hasattr(source, "read"):
            img = Image.open(source)
        else:
            raise ValueError(f"Unsupported image source type: {type(source)}")
            
        # Ensure image is in RGB format for standard model input
        if img.mode != "RGB":
            img = img.convert("RGB")
            
        return img
    except Exception as e:
        raise ValueError(f"Failed to load image: {str(e)}")
