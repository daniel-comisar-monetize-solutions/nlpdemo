FROM python:3.6.2-onbuild
EXPOSE 80
CMD exec gunicorn nlpdemo.wsgi:application --bind 0.0.0.0:80 --workers 3
