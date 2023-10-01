FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/app
RUN pip install poetry

COPY . ./

RUN poetry install --without dev

CMD ["poetry", "run", "start"]