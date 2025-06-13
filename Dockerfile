FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
