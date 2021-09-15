FROM python:3.9-slim AS base

RUN pip install --upgrade pip

WORKDIR /app

FROM base AS requirements
RUN pip install --no-cache-dir poetry==1.1.8
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt

FROM base AS final

COPY --from=requirements /app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic
RUN chmod +x dockerentrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "/app/dockerentrypoint.sh" ]
CMD [ "daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000" ]