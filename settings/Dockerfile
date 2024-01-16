FROM postgres:11.22-bullseye

ADD ./database.ddl.sql /docker-entrypoint-initdb.d
ADD ./database.dml.sql /docker-entrypoint-initdb.d

RUN chmod a+r /docker-entrypoint-initdb.d/*

EXPOSE 5432