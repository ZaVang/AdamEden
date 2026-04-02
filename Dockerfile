FROM python:3.11-slim

WORKDIR /app

# Ensure we have git inside the container if Adam wants to install from git, or curl
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Build-time install for layer caching (speeds up cold starts)
# Note: /app is bind-mounted at runtime, so the actual requirements.txt may differ
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Startup: always re-install from the bind-mounted requirements.txt
# This ensures any packages Adam writes into requirements.txt survive Docker restarts
CMD ["sh", "-c", "pip install --quiet --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && python main.py"]
