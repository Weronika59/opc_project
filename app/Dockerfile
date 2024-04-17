# Use the official Python image as base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Installing required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5005
EXPOSE 5005

# Run the application
CMD ["streamlit","run" ,"app.py", "--server.port=5005"]
