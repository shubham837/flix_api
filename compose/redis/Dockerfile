FROM redis:3.0

COPY redis-entrypoint.sh /usr/local/bin/
COPY Auth.csv /tmp/
RUN chmod +x /usr/local/bin/redis-entrypoint.sh
ENTRYPOINT ["redis-entrypoint.sh"]
