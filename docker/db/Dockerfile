FROM docker.io/postgres:latest
ENV LANG en_US.UTF-8

ADD scripts/*sql /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
