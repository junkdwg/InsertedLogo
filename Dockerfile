# 1. ใช้ Python Image ขนาดเล็ก (Alpine หรือ Slim) เพื่อประหยัดพื้นที่
FROM python:3.10-slim

# 2. ตั้งค่า Directory ทำงานภายใน Container
WORKDIR /app

# 3. ติดตั้ง Dependencies ที่จำเป็นสำหรับ Pillow (บางครั้งต้องใช้ library ของระบบ)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. คัดลอกไฟล์ requirements และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. คัดลอกโค้ดทั้งหมดเข้าเครื่อง Container
COPY . .

# 6. เปิด Port 8000 สำหรับ FastAPI
EXPOSE 8000

# 7. สั่งรัน Server ด้วย Uvicorn
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]