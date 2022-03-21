FROM python:3.8

WORKDIR .
COPY . /opt/program

RUN apt update
RUN mkdir /opt/drivers
RUN chmod 777 /opt/drivers
RUN mkdir /files
RUN chmod 777 /files
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/program/requirements.txt

#Run pip3 install pymongo
#Run pip3 install opencv-python


HEALTHCHECK CMD exit 0

CMD ["python", "/opt/program/index.py" ]