FROM python:latest
RUN mkdir /code
WORKDIR /code
RUN pip install telebot requests 
COPY ./ .
CMD [ "python", "./main.py" ]
