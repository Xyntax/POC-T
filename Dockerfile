FROM ubuntu
RUN apt-get update -y && \
    apt-get install -y python-pip
COPY ./requirements.txt  /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT [ "python" ]
CMD [ "POC-T.py" ]
