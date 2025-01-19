# Build image to install dependencies
FROM python:3.12-slim AS image
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir -r requirements.txt

# Final image with application code
FROM python:3.12-slim
COPY --from=image /usr/local/lib/python3.12/site-packages /usr/local/lib/python3/site-packages
ENV PYTHONPATH=/usr/local/lib/python3/site-packages
WORKDIR /app
COPY . /app
CMD ["python", "-m", "bot"]