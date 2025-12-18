# Official python image
FROM python:3.11-slim

# Create the workdir in the container
WORKDIR /ml

# Upgrade pip & setuptools to secure versions
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install dependencies
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/requirements.txt -r requirements/requirements-dev.txt
# -r for requirements file

COPY app/ ./app

# Port
EXPOSE 7000

# Default command
CMD ["flask", "run", "--host=0.0.0.0", "--port=7000"]