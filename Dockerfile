# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.12

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm

ENV DJANGO_ENV=production

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --no-input

# Copy the post.sh script into the container
COPY ./scripts/post.sh ./scripts/post.sh

# Convert Windows line endings to Unix line endings
RUN sed -i 's/\r$//' ./scripts/post.sh

# Make the script executable
RUN chmod +x ./scripts/post.sh

EXPOSE 8000

CMD ["/bin/sh", "-c", "./scripts/post.sh"]
