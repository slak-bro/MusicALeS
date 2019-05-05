#!/bin/sh
docker build ./docker/ -t beatdetectionarduinoengine:1.0
docker run --device /dev/snd --device /dev/ttyS2 -v $(pwd):/app -it beatdetectionarduinoengine:1.0 /app/docker/start.sh