# Hugging Face Spaces (Docker SDK)
# Listens on 7860. Runtime secrets (GEMINI_API_KEY, NANO_BANANA_API_KEY)
# are injected as env vars from the Space Settings tab — do not bake them in.

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860 \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .
RUN mkdir -p cache web_prototype/static/assets

EXPOSE 7860

# First boot trains the baseline defender (~3500 samples); logs will stall until ready.
CMD ["python", "-m", "uvicorn", "web_prototype.server:app", "--host", "0.0.0.0", "--port", "7860"]
