import base64
import io
import requests
from fastapi import HTTPException
from PIL import Image
from app.config import (
    PUB_IMG_URL,
    PUB_IMG_API_KEY,
    IMG_FETCH_TIMEOUT,
    IMG_UPLOAD_TIMEOUT,
    LOGO_WIDTH_PERCENTAGE,
    LOGO_PADDING,
    JPEG_QUALITY,
)


def get_as_base64(url: str) -> str:
    """
    Fetch an image from a URL and convert it to base64.
    
    Args:
        url: URL of the image to fetch
        
    Returns:
        Base64 encoded image string
        
    Raises:
        HTTPException: If image fetch fails
    """
    try:
        response = requests.get(url, timeout=IMG_FETCH_TIMEOUT)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch image from URL")


def process_overlay_from_b64(bg_b64: str, logo_b64: str) -> str:
    """
    Overlay a logo on a background image.
    
    Args:
        bg_b64: Base64 encoded background image
        logo_b64: Base64 encoded logo image
        
    Returns:
        Base64 encoded result image (JPEG)
    """
    # Decode and open images
    bg_img = Image.open(io.BytesIO(base64.b64decode(bg_b64))).convert("RGBA")
    logo_img = Image.open(io.BytesIO(base64.b64decode(logo_b64))).convert("RGBA")

    # Calculate logo dimensions based on background width
    bg_w, bg_h = bg_img.size
    target_logo_w = int(bg_w * LOGO_WIDTH_PERCENTAGE)
    w_percent = target_logo_w / float(logo_img.size[0])
    target_logo_h = int(float(logo_img.size[1]) * float(w_percent))
    
    # Resize logo
    logo_img = logo_img.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)

    # Position logo in top-right corner
    position = (bg_w - target_logo_w - LOGO_PADDING, LOGO_PADDING)
    bg_img.paste(logo_img, position, logo_img)

    # Convert to JPEG and encode as base64
    rgb_img = bg_img.convert("RGB")
    buffered = io.BytesIO()
    rgb_img.save(buffered, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def upload_to_oneweb(final_b64: str) -> dict:
    """
    Upload processed image to OneWeb storage service.
    
    Args:
        final_b64: Base64 encoded final image
        
    Returns:
        API response as dictionary
    """
    jpeg_binary_data = base64.b64decode(final_b64)
    file_name = "processed_image.jpg"

    payload = {
        'collection': 'PromptXAI',
        'key': PUB_IMG_API_KEY
    }
    files = [('file', (file_name, jpeg_binary_data, 'image/jpeg'))]

    try:
        response = requests.post(PUB_IMG_URL, data=payload, files=files, timeout=IMG_UPLOAD_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": "External Upload Failed", "details": str(e)}
