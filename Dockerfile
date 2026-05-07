FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (changes less frequently)
COPY ["requirements.txt",  "./"]
RUN pip install -r requirements.txt

# Copy application code (changes more frequently)
COPY [".", "./"]

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "main:app"]