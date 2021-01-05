FROM library/python:3.9.1-alpine
LABEL maintainer "Joan Font <joanfont@gmail.com>"

WORKDIR /code
ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .
ENTRYPOINT ["python3", "main.py"]
