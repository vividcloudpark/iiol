FROM python:3.12-slim

# Install system dependencies
# pyzbar requires libzbar0
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements/common.txt ./requirements/common.txt
COPY requirements/prod.txt ./requirements/prod.txt
COPY requirements.txt ./requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy project files
COPY . .

# Expose Django port
EXPOSE 8000

# Start Django using runserver or gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]