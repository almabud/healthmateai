FROM python:3.11 as web
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /webapp/
WORKDIR /webapp/
ENV HOME /webapp
COPY . /webapp

RUN python manage.py migrate

EXPOSE 8000/tcp

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

