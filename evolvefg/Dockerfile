FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

RUN chmod u+x docker_start_up.sh
RUN chmod u+x wait_db.sh
RUN sed -i -e 's/\r$//' docker_start_up.sh
RUN sed -i -e 's/\r$//' wait_db.sh