#!/bin/bash

function get_driver_version
{
    chromedriver --version | awk -F "[ .]" '{print $2}'
}

function get_browser_version
{
    (google-chrome-stable --version || \
         /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --version) 2> /dev/null | \
        awk -F "[ .]" '{print $3}'
}

export PATH=/usr/bin:$HOME/bin:$PATH

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)" > /dev/null 2>&1
  eval "$(pyenv virtualenv-init -)"
fi

os=$(uname | sed 's/Darwin/mac/; s/Linux/linux/')
driver_version=$(get_driver_version)
browser_version=$(get_browser_version)
echo "os: $os"
echo "driver: $driver_version"
echo "browser: $browser_version"

chromedriver_url=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/#stable" | perl -ne 'if (/(https:\/\/storage.googleapis.com\/chrome-for-testing-public\/'$browser_version'[\d\.]+\/'$os'[^\/]*\/chromedriver-'$os'.*?64.zip)/) { print "$1\n"; break; }')
echo "chromedriver_url: $chromedriver_url"
wget -q -nc -c "$chromedriver_url" > /dev/null
find . -maxdepth 1 -type d -name "chromedriver-$os*64" -delete > /dev/null && unzip chromedriver-$os*64.zip > /dev/null
mv chromedriver-*64/chromedriver $HOME/bin && rm -rf chromedriver-*64*
hash -r

# re-check
driver_version=$(get_driver_version)
browser_version=$(get_browser_version)
if [ "$driver_version" != "$browser_version" ]; then
    (echo "os: $os"; echo "chromedriver: $driver_version"; echo "google-chrome-stable: $browser_version") | \
        send_msg_to_gmail.py -s "chrome driver version mismatch in $os"  
fi
