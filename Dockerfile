FROM python:3

ADD . /

RUN pip install -r requirements

CMD [ "python", "./app.py" ]
