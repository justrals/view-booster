FROM python:3.9-slim

WORKDIR /view-booster

COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf-xlib-2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libfontconfig1 \
    libfreetype6 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libxkbcommon0 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install

CMD ["python", "./main.py"]