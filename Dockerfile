FROM python:3.11-slim

WORKDIR /app

# Ensure we have git inside the container if Adam wants to install from git, or curl
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Note: The code files inside /app are bind-mounted at runtime.
# But we copy requirements early so we can cache the base install
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Run command is provided by Archangel: `python main.py`
CMD ["python", "main.py"]
