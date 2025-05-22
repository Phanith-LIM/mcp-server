# Use a slim version of Python 3.12
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy poetry files first to leverage Docker layer caching
COPY pyproject.toml /app/

# Install all dependencies
RUN uv sync

# Expose the application port
EXPOSE 8000

# Copy the rest of the application
COPY . /app

# Run the application using poetry to ensure it's in the virtual environment
CMD ["fastmcp", "run", "main.py", "--transport", "sse", "--port", "8000"]