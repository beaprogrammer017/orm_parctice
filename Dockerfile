# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

RUN mkdir /blog_api

# Set the working directory
WORKDIR /blog_api

# Install dependencies
# RUN pip install --upgrade pip

# COPY requirements.txt /blog_api/


# Copy the project code into the container
COPY . /blog_api/

RUN pip install -r requirements.txt
