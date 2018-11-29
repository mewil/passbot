FROM python:alpine3.7

LABEL Author Michael Wilson

RUN pip install --upgrade \
    google-api-python-client \
    oauth2client \
    requests

COPY . /app
WORKDIR /app

CMD [ "python", "passbot.py" ]
