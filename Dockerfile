FROM python:3.12-slim

WORKDIR /app
COPY app/app.py .

ENV PORT=80
EXPOSE 80

CMD ["python", "app.py"]
