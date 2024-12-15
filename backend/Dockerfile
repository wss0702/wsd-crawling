# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.5.1

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy pyproject.toml to the container
COPY pyproject.toml /app/

# Generate poetry.lock if it doesn't exist
RUN if [ ! -f /app/poetry.lock ]; then poetry lock; fi

# Check if poetry.lock exists before copying
RUN test -f poetry.lock || touch poetry.lock

# Copy poetry.lock to the container
COPY poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8080

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000