# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/

# Copy only the requirements file to leverage Docker cache
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application with live reload
CMD ["uv","run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]