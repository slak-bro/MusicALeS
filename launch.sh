#!/bin/sh
# Launch interactive mode using -i parameter
# Otherwise all parameters are forwarded to the main.py script

printf "Building docker image ... "
OUTPUT=$(docker build ./docker/ -q -t beatdetectionarduinoengine:1.0 2>&1)
if [ $? -ne 0 ] ; then
    echo "\n\e[31mError while building image :\e[0m"
    echo "$OUTPUT"
    exit 1
else
    echo "\e[32mOK\e[0m"
fi

if [ "$1" = "-i" ] ; then
    docker run \
        --device /dev/snd \
        --device /dev/ttyS2 \
        --cap-add=SYS_NICE \
        -v $(pwd):/app \
        -it beatdetectionarduinoengine:1.0 bash -c "cd /app; bash"
else
    docker run \
        --device /dev/snd \
        --device /dev/ttyS2 \
        --cap-add=SYS_NICE \
        -v $(pwd):/app \
        -it beatdetectionarduinoengine:1.0 /app/docker/start.sh $@
fi
