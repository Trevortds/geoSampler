# Dockerfile
# buster has the wrong gdal versions
#FROM python:3.8-buster
FROM ubuntu:20.04


# install nginx
RUN apt-get update && apt-get install python3 python3-pip nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
#RUN ln -sf /var/log/stdout /var/log/nginx/access.log \
#    && ln -sf /var/log/stdout /var/log/nginx/error.log

# Install necessary dependencies for spatialite (don't need this when switched to postgres)
RUN apt-get install -y gdal-bin python3-gdal libpq-dev gcc

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/geo
COPY requirements.txt start-server.sh /opt/app/
#COPY .pip_cache /opt/app/pip_cache/
RUN true
COPY . /opt/app/geo/
RUN rm /opt/app/geo/geo/settings.py
WORKDIR /opt/app
RUN pip3 install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
RUN chmod +x /opt/app/start-server.sh

ENV DJANGO_SETTINGS_MODULE=geo.settings_deployment


# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]