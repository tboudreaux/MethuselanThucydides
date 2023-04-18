# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV TZ="America/New_York"

# Expose the port that Flask will listen on
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
