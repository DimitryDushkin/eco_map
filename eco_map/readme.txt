To run app on server use

cd /home/ubuntu/django_apps/eco_map/eco_map/
gunicorn eco_map.wsgi:application --daemon --workers=2


To reload:

cd /home/ubuntu/django_apps/eco_map/eco_map/
kill -HUP gunicorn_pid
gunicorn eco_map.wsgi:application --daemon --workers=2