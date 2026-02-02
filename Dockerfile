FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# ========= 基础依赖 =========
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    wget \
    ca-certificates \
    gnupg \
    unzip \
    fonts-liberation \
    libasound2 \
    libnss3 \
    libxss1 \
    libx11-xcb1 \
    libgbm1 \
    libgtk-3-0 \
    libdrm2 \
    && rm -rf /var/lib/apt/lists/*

# ========= 安装 Chrome for Testing（官方） =========
WORKDIR /tmp

RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/145.0.7632.26/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/local/bin/google-chrome && \
    rm -f chrome-linux64.zip

RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/145.0.7632.26/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64*

# ========= Python 依赖 =========
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# ========= 拷贝脚本 =========
COPY meet.py /app/meet.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
