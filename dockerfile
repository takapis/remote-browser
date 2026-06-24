FROM python:3.11-slim

# Chrome と依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN wget -q https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE && \
    VERSION=$(cat LATEST_RELEASE_STABLE) && \
    wget -q https://edgedl.selenium.dev/chrome-driver/${VERSION}/linux64/chromedriver-linux64.zip && \
    apt-get update && apt-get install -y unzip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 10000

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
