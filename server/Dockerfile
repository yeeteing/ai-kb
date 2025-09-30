FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

## copy app code
COPY . .


# envs (override via compose or cloud)
ENV APP_ENV=development \
    PORT=8000 \
    HOST=0.0.0.0

# expose port & run uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]