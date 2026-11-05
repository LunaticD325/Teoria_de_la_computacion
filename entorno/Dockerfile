ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLET_FORCE_WEB_SERVER=true
ENV FLET_SERVER_PORT=8550

CMD ["python", "src/app.py"]