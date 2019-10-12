FROM postgres:12

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update
RUN apt-get -y install python3 python3-pip postgresql-plpython3-12 libssl-dev libpq-dev libgmp-dev

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install music21

ADD py /smrpy
ENV PYTHONPATH=/
RUN pip3 install -r /smrpy/requirements.txt
