FROM python:3.12-rc-alpine

RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    libpq-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY dist/travel_box_api-*.tar.gz /app

RUN python3 -m pip install --no-cache-dir travel_box_api-*.tar.gz

RUN python3 -m pip install --no-cache-dir gunicorn

EXPOSE 5000

# Travel is not yet ThreadSafe : -w 1 
CMD ["python3", "-m", "gunicorn", "-w", "1", "-b", "127.0.0.1:5000", "--timeout", "600", "travel_box_api.__main__:app"]
