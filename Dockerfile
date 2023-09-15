FROM python:3.9.18-slim-bullseye
WORKDIR /app
RUN apt update && apt install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

RUN PATH="$PATH:/root/.local/bin" poetry config virtualenvs.create false
RUN PATH="$PATH:/root/.local/bin" poetry install

COPY app.py /app/app.py

EXPOSE 7860
ENV GRADIO_SERVER_NAME=0.0.0.0
CMD python3 app.py

