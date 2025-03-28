FROM python:3.11-slim
RUN pip install flask yt-dlp
COPY app.py .
CMD ["python", "app.py"]