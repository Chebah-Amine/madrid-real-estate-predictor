# Use official Python image
FROM python:3.11-slim

# Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # UV cache directory
    UV_CACHE_DIR=/root/.cache/uv

# Create workdir
WORKDIR /stats

# Install uv (ultra-fast Python package installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy only requirements files first (for better Docker layer caching)
COPY requirements/ ./requirements/

# Install dependencies with uv cache enabled
# This layer is cached unless requirements change
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system \
    -r requirements/requirements.txt \
    -r requirements/requirements-dev.txt

# Copy application code (changes frequently, so this layer is separate)
COPY app/ ./app

# Copy coverage configuration
COPY .coveragerc ./

# Expose port
EXPOSE 7005

# Default command
CMD ["flask", "run", "--host=0.0.0.0", "--port=7005"]