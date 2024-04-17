# Use the official Python image as base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# For eventually problems with libraries installation
RUN pip cache purge

# Installing required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the uvicorn service
CMD ["uvicorn", "preprocess:app", "--host", "0.0.0.0", "--port", "5000"]