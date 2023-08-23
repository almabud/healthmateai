FROM python:3.11 as web
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /webapp/
WORKDIR /webapp/
ENV HOME /webapp
COPY . /webapp

RUN python manage.py migrate
RUN python manage.py collectstatic -v 2 --noinput

EXPOSE 8000/tcp

# Set the command to run your Django app
CMD ["gunicorn", "healthmateai.wsgi:application", "--bind", "0.0.0.0:8000"]

