FROM python:3.12-slim-bullseye

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY endpoint.py .
COPY configs.py .
COPY templates templates

CMD ["uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
