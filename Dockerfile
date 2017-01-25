FROM python:3.4

RUN apt-get update
RUN yes '' | apt-get install mysql-client
RUN yes '' | apt-get install libqt4-dev
RUN yes '' | apt-get install cmake
RUN yes '' | apt-get install xdelta
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install pyside
RUN pip install configobj

RUN apt-get update
RUN yes '' | apt-get install xdelta3
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD . /code/

COPY passwords.example.py /code/passwords.py

WORKDIR /code/

CMD ./serverUpdater.py

EXPOSE 9001
