from pathlib import Path
from config.settings import SUPPORTED_FORMATS, MAX_IMAGE_SIZE

def variable_image_file(file_path: str) -> tuple[bool, str]:
    path = Path(file_path)
    if not path.exists():
        return False, "File does not exist"
    
    if not path.is_file():
        return False, "Path is not a file."
    # Check file extension
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        return False, f"Unsupported format. Supported: {", ".join(SUPPORTED_FORMATS)}"
    
    file_size = path.stat().st_size
    if file_size > MAX_IMAGE_SIZE:
        max_mb = MAX_IMAGE_SIZE / (1024 * 1024)
        actual_mb = file_size / (1024 * 1024)
        return False, f"File too large. Max: {max_mb:.1f}MB, Actual: {actual_mb:.1f}MB"

    if file_size == 0:
        return False, "File is empty"

    return True, ""
