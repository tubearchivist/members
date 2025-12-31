FROM python:3.13.11-slim-trixie
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --user -r requirements.txt

RUN mkdir /app
COPY client /app
WORKDIR /app

ENTRYPOINT ["python", "client.py"]
