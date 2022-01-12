FROM python:3.7

#RUN python -m pip install --upgrade pip 
    #pip3 install -r requirements.txt

RUN pip3 install fastapi uvicorn jinja2 sqlalchemy

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host","0.0.0.0", "--port", "15400" ]