FROM python:3.12.0-alpine3.18

ENV BUILD_PACKAGES=""
RUN apk --update --upgrade --no-cache add $BUILD_PACKAGES

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "script.py"]
