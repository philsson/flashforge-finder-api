FROM python:3.5

RUN apt-get update -y && apt-get install -y python-pip python-dev git

COPY ./ /app

WORKDIR /app/api

RUN pip install -r ../requirements.txt

ENV FLASK_APP=webapi.py

# Expose the application's port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]