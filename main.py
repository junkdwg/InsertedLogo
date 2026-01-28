from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import PIL.Image as Image
import io, base64, requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- CONFIGURATION ---
URL = os.getenv('PUB-IMG-URL')
IMG_API_KEY = os.getenv('PUB-IMG-API-KEY')
BEARER_AUTH_KEY = os.getenv('BEARER_AUTH_KEY', 'BEARER_AUTH_KEY')

auth_scheme = HTTPBearer()

# --- SECURITY LOGIC ---
def validate_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):

    if credentials.credentials != BEARER_AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Bearer Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# --- MODELS ---
class ImageUrlRequest(BaseModel):
    image_url: str
    logo_url: str

class ImageOverlayResponse(BaseModel):
    api_response: dict
    status: str

# --- HELPER FUNCTIONS ---
def get_as_base64(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except Exception:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL")

def process_overlay_from_b64(bg_b64: str, logo_b64: str) -> str:
    
    bg_img = Image.open(io.BytesIO(base64.b64decode(bg_b64))).convert("RGBA")
    logo_img = Image.open(io.BytesIO(base64.b64decode(logo_b64))).convert("RGBA")

    bg_w, bg_h = bg_img.size
    target_logo_w = int(bg_w * 0.20)
    w_percent = (target_logo_w / float(logo_img.size[0]))
    target_logo_h = int((float(logo_img.size[1]) * float(w_percent)))
    logo_img = logo_img.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)

    padding = 20
    position = (bg_w - target_logo_w - padding, padding)
    bg_img.paste(logo_img, position, logo_img)

    rgb_img = bg_img.convert("RGB")
    buffered = io.BytesIO()
    rgb_img.save(buffered, format="JPEG", quality=90, optimize=True)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def upload_to_oneweb(final_b64: str) -> dict:
    
    jpeg_binary_data = base64.b64decode(final_b64)
    file_name = "processed_image.jpg"

    
    payload = {
        'collection': 'PromptXAI',
        'key': IMG_API_KEY
    }
    files = [('file', (file_name, jpeg_binary_data, 'image/jpeg'))]

    try:
        response = requests.post(URL, data=payload, files=files, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": "External Upload Failed", "details": str(e)}

# --- ENDPOINT ---

@app.post("/overlay-logo", response_model=ImageOverlayResponse)
async def overlay_api(request: ImageUrlRequest, _=Depends(validate_bearer_token)):
    print(f"DEBUG: Received request: {request.dict()}")
    try:
        bg_b64 = get_as_base64(request.image_url)
        logo_b64 = get_as_base64(request.logo_url)
        final_b64 = process_overlay_from_b64(bg_b64, logo_b64)
        raw_api_result = upload_to_oneweb(final_b64)
        
        return {
            "api_response": raw_api_result,
            "status": "success"
        }
    except Exception as e:
        # error
        raise HTTPException(status_code=500, detail="An internal error occurred during processing")