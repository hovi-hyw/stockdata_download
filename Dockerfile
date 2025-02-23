# Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

# 安装 Poetry
RUN pip install poetry==1.7.1

# 使用 Poetry 安装依赖
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "scripts/run_tasks.py"]