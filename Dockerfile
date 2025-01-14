FROM python:3.12-rc-alpine

COPY app/ .

["gunicorn", "-w", "20", "-b", "127.0.0.1:8083", "main:app"]
