#!/bin/bash

export PATH=/usr/bin:/home/terzeron/bin

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)" > /dev/null 2>&1
  eval "$(pyenv virtualenv-init -)"
fi

driver_version=$(chromedriver --version | awk -F "[ .]" '{print $2}')
browser_version=$(google-chrome-stable --version | awk -F "[ .]" '{print $3}')

if [ "$driver_version" != "$browser_version" ]; then
    (echo "chromedriver: $driver_version"; echo "google-chrome-stable: $browser_version") | \
        send_msg_to_gmail.py -s "chrome driver version mismatch" 
fi
