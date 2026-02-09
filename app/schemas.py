from pydantic import BaseModel


class ImageUrlRequest(BaseModel):
    """Request model for image overlay endpoint"""
    image_url: str
    logo_url: str


class ImageOverlayResponse(BaseModel):
    """Response model for image overlay endpoint"""
    api_response: dict
    status: str
