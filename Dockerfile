FROM python:3.10.4-slim-buster

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "app.py"]




