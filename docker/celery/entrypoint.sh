#!/usr/bin/env bash

exec celery -A dj_main worker "$@"
