FROM postgres:11

ADD --chown=postgres ./sql/* /docker-entrypoint-initdb.d/
RUN chown -R postgres /docker-entrypoint-initdb.d