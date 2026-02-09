from fastapi import APIRouter, HTTPException, Depends

from app.schemas import ImageUrlRequest, ImageOverlayResponse
from app.security import validate_bearer_token
from app.utils import get_as_base64, process_overlay_from_b64, upload_to_oneweb

router = APIRouter(prefix="/api", responses={404: {"description": "Not found"}})


@router.post("/overlay-logo", response_model=ImageOverlayResponse)
async def overlay_api(request: ImageUrlRequest, _=Depends(validate_bearer_token)):
    """
    Overlay a logo on a background image and upload the result.
    
    Args:
        request: ImageUrlRequest with image_url and logo_url
        _: Bearer token validation dependency
        
    Returns:
        ImageOverlayResponse with API response and status
        
    Raises:
        HTTPException: On processing errors
    """
    try:
        bg_b64 = get_as_base64(request.image_url)
        logo_b64 = get_as_base64(request.logo_url)
        final_b64 = process_overlay_from_b64(bg_b64, logo_b64)
        raw_api_result = upload_to_oneweb(final_b64)
        
        return {
            "api_response": raw_api_result,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred during processing")
