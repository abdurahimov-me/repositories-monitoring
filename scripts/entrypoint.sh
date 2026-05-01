#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=core.settings.prod

echo "Starting supervisor..."
exec supervisord -c /scripts/supervisord.conf
