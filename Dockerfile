FROM python:3.9

ENV VENV_PATH="/venv"
ENV PATH="$VENV_PATH/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade poetry
RUN python -m venv /venv

COPY . .

RUN poetry build && \
    /venv/bin/pip install --upgrade pip wheel setuptools &&\
    /venv/bin/pip install dist/*.whl

CMD bhagavad-gita-api
