FROM python:3.7-slim

WORKDIR /app

RUN pip install pipenv

COPY ./src ./src/
COPY src/app.py .
COPY Pipfile .

RUN pipenv install --skip-lock --deploy --system

ARG APP_PORT

ENV APP_PORT ${APP_PORT:-'5001'}

ENV PYTHONPATH=/usr/local/lib/python3.7/
ENV PYTHONPATH=${PYTHONPATH}:/app/src

ENV TZ=America/Sao_Paulo
ENV USER_LANGUAGE=pt
ENV USER_COUNTRY=BR

EXPOSE ${APP_PORT}

CMD python app.py
