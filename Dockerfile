FROM python:3.7-slim-stretch as dev

#WORKDIR /app
RUN apt update && apt install -y libpq-dev python-dev build-essential

COPY ./requirements.txt /app//requirements.txt
RUN pip3 install -r /app/requirements.txt

#RUN pip3 install fastapi uvicorn jinja2 sqlalchemy

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host","0.0.0.0", "--port", "15400" ]