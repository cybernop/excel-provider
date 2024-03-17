FROM python:3.11 as builder

RUN pip install -U pip wheel
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .
COPY src .

ARG package_version=prepatch
RUN poetry version $package_version
RUN poetry build


FROM python:3.11 as runner

RUN pip install -U pip wheel

WORKDIR /app

COPY --from=builder /app/dist/*.whl ./dist/
RUN pip install --find-link=./dist excel_provider

EXPOSE 5000

ENTRYPOINT [ "python", "-m", "excel_provider" ]
CMD [ "--config", "config.yaml" ]
