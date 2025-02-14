# Use an official lightweight Python image
FROM python:3.12.7

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (if any are needed, e.g., build tools)
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure modern PEP 621 support
RUN pip install --upgrade pip

# Copy only the dependency management files first for caching purposes
# (If you have a setup.cfg or setup.py, copy them as well)
COPY pyproject.toml ./

# Copy the rest of your application code
COPY . .

# Install your package along with its dependencies
RUN pip install .

# Expose the port on which your app will run
EXPOSE 80

# Run the app using Uvicorn (adjust "app.main:app" as needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]