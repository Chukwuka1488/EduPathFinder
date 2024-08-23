# backend/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=$PATH:/home/appuser/.local/bin

# Install only necessary packages
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set the working directory
RUN addgroup --gid 1001 appgroup && \
    adduser --disabled-password --gecos '' --uid 1001 --gid 1001 appuser

# Set the working directory in the container to /app
WORKDIR /app

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary port
EXPOSE 5001

# Healthcheck for the container
HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/health || exit 1

# # Accept build arguments and set them as environment variables
# ARG azure-client-id
# ARG azure-client-secret
# ARG azure-tenant-id
# ARG cosmosconnectionstring
# ARG cosmosdb-account-name
# ARG keyvault-name

# ENV azure-client-id=$azure-client-id
# ENV azure-client-secret=$azure-client-secret
# ENV azure-tenant-id=$azure-tenant-id
# ENV cosmosconnectionstring=$cosmosconnectionstring
# ENV cosmosdb-account-name=$cosmosdb-account-name
# ENV keyvault-name=$keyvault-name

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:create_app()"]
