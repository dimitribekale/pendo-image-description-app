from PIL import Image
import base64
from io import BytesIO

class ImageService:

    """Handles image operations."""
    @staticmethod
    def validate_image(file_path: str) -> bool:
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False
        
    @staticmethod
    def get_image_info(file_path: str) -> dict:
        """Get image metadata"""
        with Image.open(file_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
            }
        
    @staticmethod
    def resize_image(file_path: str, max_size: tuple = (1024, 1024)) -> Image.Image:
        """Resize image while maintaining aspect ratio."""
        img = Image.open(file_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        return img
    
    @staticmethod
    def image_to_base64(file_path: str, max_size: tuple=(1024, 1024)) -> str:
        """Convert image to Base64 string for API transmission."""
        img = ImageService.resize_image(file_path, max_size)
        buffered = BytesIO()
        # Convert to RGB if necessary (for RGBA images)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        img.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    @staticmethod
    def get_image_bytes(file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            return f.read()

