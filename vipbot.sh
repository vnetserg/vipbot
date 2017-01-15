#!/usr/bin/env bash

# Check that virtual environment exists
#
if [[ ! -e "/opt/vipbot/bin/activate" ]]; then
    echo "CRITICAL: no virtual environment found under /opt/vipbot"
    exit 1
fi

# Activate virtualenv
source /opt/vipbot/bin/activate

# Execute vipbot
exec python -m vipbot ${@:1}
