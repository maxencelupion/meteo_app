FROM python:latest

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["flask", "run", "--port=5000"]
