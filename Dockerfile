# Use the Python 3.12 base image
FROM python:3.12.6-slim

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Set the working directory and copy the application code
WORKDIR /app
COPY . /app

# Start the bot
CMD ["python", "-m", "bot"]
