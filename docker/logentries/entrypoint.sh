#!/usr/bin/env bash

exec /usr/src/app/index.js --no-stats \
                            -j \
                            -a host=`uname -n` \
                            -l $LOGSTOKEN \
                            -e $EVENTSTOKEN \
                            --skipByImage '.*(docker-nginx-entrypoint|amazon-ecs-agent).*'
