#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=config.settings.production

echo "Starting supervisor..."
exec supervisord -c /scripts/supervisord.conf
