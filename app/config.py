import os
from dotenv import load_dotenv

load_dotenv()

# Image API Configuration
PUB_IMG_URL = os.getenv('PUB-IMG-URL')
PUB_IMG_API_KEY = os.getenv('PUB-IMG-API-KEY')

# Security Configuration
BEARER_AUTH_KEY = os.getenv('BEARER_AUTH_KEY')

# Application Configuration
IMG_UPLOAD_TIMEOUT = 30  # seconds
IMG_FETCH_TIMEOUT = 10  # seconds
LOGO_WIDTH_PERCENTAGE = 0.20  # 20% of background image width
LOGO_PADDING = 20  # pixels
JPEG_QUALITY = 90
