FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /

# Install dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /

# Expose the port that Django will run on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app_dashboard_backend.wsgi:application"]
