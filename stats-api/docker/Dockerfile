FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /stats

RUN pip install --no-cache-dir --upgrade pip setuptools

COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/requirements.txt -r requirements/requirements-dev.txt

# utile pour le mode "prod" (sans volume). En dev, le volume écrasera /stats/app
COPY app/ ./app

COPY .coveragerc ./

EXPOSE 7005

CMD ["flask", "run", "--host=0.0.0.0", "--port=7005"]
