FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY . /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

CMD ["poetry", "run", "python", "-m", "litestar", "run", "--host", "0.0.0.0", "--port", "8000"]