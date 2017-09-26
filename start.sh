#!/usr/bin/env bash

exec gunicorn nlpdemo.wsgi:application --bind 0.0.0.0:80 --workers 3
