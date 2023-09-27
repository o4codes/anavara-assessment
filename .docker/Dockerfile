# Use an official Python runtime as the base image
FROM python:3.10


# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install the PostgreSQL client library
RUN apt-get update && apt-get install -y libpq-dev

# Copy the requirements file and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /app/
RUN chmod +x .docker/dev_web_entrypoint.sh
ENTRYPOINT [".docker/dev_web_entrypoint.sh"]