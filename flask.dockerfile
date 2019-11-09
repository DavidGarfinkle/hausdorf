### Website ###
FROM alpine:latest AS webapp-build
RUN apk add --update --no-cache \
    nodejs nodejs-npm
ADD ./webclient/package*.json /webclient/
WORKDIR /webclient
RUN npm install
ADD ./webclient .
RUN node_modules/webpack/bin/webpack.js --mode development

### Virtualenv ###
FROM python:3.7.4 AS venv-image
RUN pip3 install virtualenv
RUN virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install flask uwsgi
RUN pip3 install music21
RUN pip3 install grpcio grpcio-tools
RUN pip3 install numpy pandas

### Flask ###
FROM python:3.7.4
COPY --from=venv-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /cbsmr

ADD ./Makefile .
ADD ./proto ./proto
RUN make proto/smr_pb2.py proto/smr_pb2_grpc.py

ADD ./requirements.txt ./smrpy/requirements.txt
RUN pip3 install -r ./smrpy/requirements.txt

ADD ./smrpy/ ./smrpy/
ENV PYTHONPATH=/cbsmr
COPY --from=webapp-build /webclient/src/*.html /cbsmr/smrpy/templates/search.html
COPY --from=webapp-build /webclient/dist/*.js /cbsmr/smrpy/templates/search.js
COPY --from=webapp-build /webclient/favicon.ico /cbsmr/smrpy/templates/

WORKDIR /cbsmr/smrpy
CMD ["uwsgi", "--module", "smrpy.app", "--uwsgi-socket", "socket/uwsgi.sock", "--chmod-socket=666", "--workers", "3", "--vacuum", "--die-on-term", "--master"]
