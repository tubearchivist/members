FROM python:3.11.3-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --user -r requirements.txt

RUN mkdir /app
COPY client /app
WORKDIR /app

ENTRYPOINT ["python", "client.py"]
