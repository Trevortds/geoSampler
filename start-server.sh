#!/usr/bin/env bash
# start-server.sh

if [ -z $POSTGIS_PORT ] ; then
  POSTGIS_PORT=5432
fi

echo "waiting for server to start"
while !</dev/tcp/$POSTGIS_HOST/$POSTGIS_PORT; do sleep 1; done;

echo "Apply database migrations"
(cd geo; python manage.py migrate auth)
(cd geo; python manage.py migrate)

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] ; then
#    (cd geo; python manage.py createsuperuser --no-input --email $DJANGO_SURERUSER_EMAIL \
#            --username $DJANGO_SUPERUSER_USERNAME)
    echo "Creating superuser"
    (cd geo; python ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')")
fi

echo "collect static files"
(cd geo; python manage.py collectstatic --noinput)


echo "Start Server"
(cd geo; gunicorn geo.wsgi  --user www-data --bind 0.0.0.0:8010 --workers 3 ) &
#(cd geo; gunicorn geo.wsgi --log-level debug --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
#  --user www-data --bind 0.0.0.0:8010 --workers 3 2>/var/log/stderr 1>/var/log/stdout) &
nginx -g "daemon off;"

#tail -qf --follow=name --retry /var/log/stdout /var/log/stderr
