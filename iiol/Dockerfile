FROM ubuntu:18.04

RUN apt-get update && \
apt-get install -y python3-pip python3-dev &&\
 apt-get clean

WORKDIR /djangoproject
ADD . /djangoproject
RUN pip3 install -r requirements.txt



EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "iioi.wsgi:application", "--bind", "0.0.0.0:80"]