FROM python:3.11-slim

# Create app directory
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port and start FastAPI app
EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
