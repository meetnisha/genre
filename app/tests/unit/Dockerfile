FROM python:3.7-slim-stretch as devtests
LABEL maintainer="Manisha Pradhan <manisha.pradhan3008@gmail.com>"

RUN python -m ensurepip && pip install --upgrade pip

RUN pip3 install pytest-cov

COPY ./tests/unit/requirements.txt /apps/requirements.txt

WORKDIR /apps

RUN pip3 install --force-reinstall -r requirements.txt

COPY ./tests/unit/test_main.py /apps/test_main.py