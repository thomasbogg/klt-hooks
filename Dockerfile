FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (changes less frequently)
COPY ["requirements.txt",  "./"]
RUN pip install -r requirements.txt

# Copy application code (changes more frequently)
COPY [".", "./"]

EXPOSE 8000

CMD ["python", "main.py"]