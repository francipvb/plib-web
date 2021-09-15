# Python base image: Here we can add dependencies used both at build-time and final image.
FROM python:3.9-slim AS base

WORKDIR /app

FROM base AS requirements

RUN pip install --no-cache-dir poetry==1.1.8
COPY pyproject.toml poetry.lock ./

# This is to avoid the inclusion of poetry in the final image. It is not needed at runtime.
RUN poetry export -f requirements.txt -o requirements.txt

FROM node:latest AS frontend

WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend ./
RUN yarn build --output-path=build/frontend

FROM base AS final

# Get the built requirements file to install dependencies:
COPY --from=requirements /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Project files
COPY . .

# And the built front-end application:
COPY --from=frontend /app/frontend/build ./frontend/dist/

# Django needs static files in a single folder for all apps, so we need this:
RUN python manage.py collectstatic

# Entrypoint - This is to run migrations, for example.
RUN chmod +x dockerentrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "/app/dockerentrypoint.sh" ]
CMD [ "daphne", "config.asgi:application", "-b", "0.0.0.0", "-p", "8000" ]
