FROM python:3.10.8-slim-bullseye
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH

COPY client/requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --user -r requirements.txt

RUN mkdir /app
COPY ./client/src /app
WORKDIR /app

ENTRYPOINT ["python", "client.py"]
