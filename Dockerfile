FROM python:3.12-slim
WORKDIR /burial
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY main.py .
RUN useradd --create-home burial && mkdir -p data logs && chown -R burial:burial /burial
USER burial
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
CMD ["python", "main.py", "run"]
