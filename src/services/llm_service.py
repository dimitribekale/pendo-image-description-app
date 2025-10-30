import torch
from config.settings import (
    HUGGINGFACE_MODEL,
    HUGGINGFACE_DEVICE,
    MODELS_CACHE_DIR,
)
from src.services.image_service import ImageService


class LLMService:
    """
    Loading a HuggingFace model.
    """
    def __inti__(self):
        self.image_service = ImageService()
        self._hf_pipeline = None

    def analyze_image(self, image_path: str) -> str:
        """
        The model analyzes the image and returns 
        the result as a string.
        """
        return self._analyze_with_huggingface(image_path)
    
    def _analyze_with_huggingface(self, image_path: str) -> str:
        """Inference using the model."""

        try:
            from tranformers import pipeline
            from PIL import Image

            if self._hf_pipeline is None:
                device_map = self._get_device()
                print(f"Loading the model from HuggingFace: {HUGGINGFACE_MODEL}")
                print(f"Using device: {device_map}")

                if device_map == "mps": # Apple Silicon (MPS)
                    self._hf_pipeline = pipeline(
                        "image-to-text",
                        model=HUGGINGFACE_MODEL,
                        device=device_map,
                        model_kwargs={"cache_dir": str(MODELS_CACHE_DIR)}
                    )
                elif device_map == -1:
                    # CPU mode
                    self._hf_pipeline = pipeline(
                        "image-to-text",
                        model=HUGGINGFACE_MODEL,
                        device=None,
                        model_kwargs={"cache_dir": str(MODELS_CACHE_DIR)}
                    )
                else:
                    # CUDA
                    self._hf_pipeline = pipeline(
                        "image-to-text",
                        model=HUGGINGFACE_MODEL,
                        device=device_map,
                        model_kwargs={"cache_dir": str(MODELS_CACHE_DIR)}
                    )
                print("Model loaded successfully!")

            image = Image.open(image_path)

            # Generate the description
            result = self._hf_pipeline(image)

            # Extract the text from result
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get("generated_text", "No description generated")
            else:
                text = str(result)

            output = f"""
                        AI-based Image Description
                        Model: {HUGGINGFACE_MODEL.split("/")[-1]}
                        Device: {self._get_device()}
                        
                        Description:
                        {text}

                        Analysis complete!
                        """
            return output
        
        except ImportError as e:
            return (
                f"Failed to import the tranformers library.\n\n"
                f"More Details here: {str(e)}"
            )
        except Exception as e:
            raise Exception(f"HuggingFace mode error; {str(e)}")
        
    def _get_device(self):

        if HUGGINGFACE_DEVICE == "auto":
            if torch.cuda.is_available():
                print("Using CUDA for inference.")
                return 0
            elif torch.backends.mps.is_available():
                print("Using Apple Silicon (MPS) GPU for inference.")
                return "mps"
            else:
                print("Using CPU for inference.")
                return -1

        elif HUGGINGFACE_DEVICE == "cuda":
            if torch.cuda.is_available():
                print("Using CUDA for inference")
                return 0
            else:
                print("CUDA not available... Using CPU.")
                return -1
            
        elif HUGGINGFACE_DEVICE == "mps":
            if torch.backends.mps.is_available():
                print("Using Apple Silicon (MPS) GPU inference.")
                return "mps"
            else:
                print("No MPS available... Using CPU.")
                return -1
            
        else:
            print("Using CPU for inference.")
            return -1
