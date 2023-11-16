FROM python:3.10
WORKDIR /app

ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Run Celery worker and beat
CMD ["celery", "-A", "lynkly.celery", "worker", "--loglevel=info", "--concurrency=4"]
CMD ["celery", "-A", "lynkly.celery", "beat", "--loglevel=info"]

# Start Gunicorn
ENTRYPOINT ["gunicorn", "lynkly.wsgi"]
