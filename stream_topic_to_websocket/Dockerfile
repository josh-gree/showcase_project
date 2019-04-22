FROM python:3.7

RUN mkdir -p /src/app
ADD ./Pipfile* /src/app/

WORKDIR /src/app
RUN pip install pipenv && pipenv install --deploy
ADD ./src .

ENTRYPOINT pipenv run python stream_topic_to_websocket.py