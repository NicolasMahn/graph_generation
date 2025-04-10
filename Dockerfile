# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Set build arguments for secrets
ARG BACKEND_HOST
ARG BACKEND_PORT
ARG CHROMADB_HOST
ARG CHROMADB_PORT
ARG OPENAI_KEY
ARG GOOGLE_KEY

# Set environment variables for secrets
ENV BACKEND_HOST=${BACKEND_HOST}
ENV BACKEND_PORT=${BACKEND_PORT}
ENV CHROMADB_HOST=${CHROMADB_HOST}
ENV CHROMADB_PORT=${CHROMADB_PORT}
ENV OPENAI_KEY=${OPENAI_KEY}
ENV GOOGLE_KEY=${GOOGLE_KEY}

# Run main.py when the container launches
CMD ["python", "main.py"]