#!/bin/sh
set -e

USER=${USER:-"fruit-store:fruit-store"}
CMD="fruit-store"

# SERVER RUNNING UNPRIVILEDGED
CMD_SERVER="gosu $USER tini -- $CMD server"

# CLIENT RUNNING AS ROOT BUT UNDER TINI FOR GUARANTEED DOWN.
CMD_CLIENT="tini -- $CMD client"

if [ "$(id -u)" = '0' ]; then
    chown -R "$USER" . || exit 1
    # chmod 700 . || exit 2
fi

# this if will check if the first argument is a flag
# but only works if all arguments require a hyphenated flag
# -v; -SL; -f arg; etc will work, but not arg1 arg2
if [ "$#" -eq 0 ] || [ "${1#-}" != "$1" ]; then
    set -- "$CMD" "$@"
fi

# TODO: INCLUDE BOOTSTRAPING SCRIPTS IF ONE MUST
#DATA_PATHS="/var/db"

for d in $DATA_PATHS
do
    if [ -d "$d" ]; then
        chown "$USER" "$d"
    fi
done

# check for the expected command
if [ "$1" = 'server' ]; then
    shift
    exec $CMD_SERVER $@
fi

if [ "$1" = 'client' ]; then
    shift
    exec $CMD_CLIENT $@
fi

if [ "$1" = 'healthcheck' ]; then
    shift
    exec $CMD_CLIENT "healthcheck"
fi

# else default to run whatever the user wanted like "bash" or "sh"
exec "$@"
