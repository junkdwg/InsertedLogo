# InsertedLogo API

A FastAPI-based microservice for overlaying logos on images and uploading them to cloud storage.

## Overview

This API processes images by:
1. Fetching a background image and logo from URLs
2. Overlaying the logo in the top-right corner (20% of image width)
3. Uploading the processed image to OneWeb storage
4. Returning the API response

## Project Structure

```
InsertedLogo/
├── app/
│   ├── __init__.py              # App factory (create_app)
│   ├── config.py                # Configuration & environment variables
│   ├── schemas.py               # Pydantic request/response models
│   ├── security.py              # Bearer token authentication
│   ├── utils.py                 # Image processing & upload functions
│   └── routes/
│       ├── __init__.py
│       └── overlay.py           # POST /api/overlay-logo endpoint
├── tests/
│   ├── __init__.py
│   └── test_overlay.py          # Unit tests for endpoints
├── main.py                      # Entry point (uvicorn)
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yaml          # Docker compose configuration
├── .env                         # Environment variables (not in repo)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Setup

### Prerequisites
- Python 3.10+
- Docker (optional)
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd InsertedLogo
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

**Required environment variables:**
```env
PUB-IMG-URL=https://your-upload-service.com/upload
PUB-IMG-API-KEY=your-api-key
BEARER_AUTH_KEY=your-secret-token
```

## Running the Application

### Local Development

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or using Python
python main.py
```

Server will run on `http://localhost:8000`

### Docker

```bash
# Build and run
docker-compose up --build

# Just run (if already built)
docker-compose up

# Stop
docker-compose down
```

## API Documentation

### Interactive API Docs
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Endpoint: Overlay Logo

**POST** `/api/overlay-logo`

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "image_url": "https://example.com/image.jpg",
  "logo_url": "https://example.com/logo.png"
}
```

**Response (Success 200):**
```json
{
  "api_response": {
    "url": "https://storage.example.com/image.jpg",
    "status": "uploaded"
  },
  "status": "success"
}
```

**Response (Auth Error 401):**
```json
{
  "detail": "Invalid Bearer Token"
}
```

### Example Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/overlay-logo" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://via.placeholder.com/800x600",
    "logo_url": "https://via.placeholder.com/100x100"
  }'
```

### Example Request (Postman/REST Client)

```
POST http://localhost:8000/api/overlay-logo

Headers:
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

Body:
{
  "image_url": "https://via.placeholder.com/800x600",
  "logo_url": "https://via.placeholder.com/100x100"
}
```

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_overlay.py
```

### Run with Verbose Output
```bash
pytest tests/test_overlay.py -v
```

### Run Specific Test
```bash
pytest tests/test_overlay.py::test_overlay_missing_auth -v
```

## Configuration

All configuration is managed in `app/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PUB_IMG_URL` | - | OneWeb upload endpoint |
| `PUB_IMG_API_KEY` | - | API key for upload service |
| `BEARER_AUTH_KEY` | - | Bearer token for authentication |
| `IMG_UPLOAD_TIMEOUT` | 30 | Upload request timeout (seconds) |
| `IMG_FETCH_TIMEOUT` | 10 | Image fetch timeout (seconds) |
| `LOGO_WIDTH_PERCENTAGE` | 0.20 | Logo width as % of image (20%) |
| `LOGO_PADDING` | 20 | Logo padding from edge (pixels) |
| `JPEG_QUALITY` | 90 | Output JPEG quality (0-100) |

## Image Processing Details

- **Logo Placement:** Top-right corner
- **Logo Sizing:** 20% of background image width (maintains aspect ratio)
- **Output Format:** JPEG with 90% quality
- **Image Handling:** Both images converted to RGBA for transparency support

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **pillow** - Image processing
- **requests** - HTTP requests
- **python-dotenv** - Environment variables
- **pytest** - Testing framework
- **httpx** - Async HTTP client for testing

## Docker Deployment

The `Dockerfile` includes:
- Python 3.10-slim base image
- System dependencies for image processing (libjpeg, zlib)
- All Python requirements
- Uvicorn server on port 8000

The `docker-compose.yaml` configuration:
- Exposes port 8000
- Loads `.env` file automatically
- Auto-restart on failure
- Container name: `insertedlogo-api`

## Error Handling

| Status | Reason |
|--------|--------|
| 401 | Invalid or missing Bearer token |
| 400 | Failed to fetch image from URL |
| 500 | Internal processing error |

## Best Practices

✅ Security:
- Bearer token authentication
- No credentials in code
- Environment variables for secrets

✅ Code Quality:
- Modular structure
- Type hints with Pydantic
- Comprehensive docstrings
- Unit tests included

✅ Maintainability:
- Separation of concerns
- Reusable utility functions
- Centralized configuration
- Ready to scale

## Future Enhancements

- [ ] Add logging and monitoring
- [ ] Implement rate limiting
- [ ] Add multiple logo positioning options
- [ ] Support batch image processing
- [ ] Add webhook notifications
- [ ] Cache processed images
- [ ] Add image format options (PNG, WebP, etc.)

## License

[Add your license here]

## Support

For issues or questions, please open an issue in the repository.

 
