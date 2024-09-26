# Use an official Python runtime as a parent image
FROM python:3.9-slim

COPY requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV NAME LLM-RAG
ENV PYTHONPATH=/opt/project/LLM-RAG

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app