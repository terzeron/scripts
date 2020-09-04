#!/bin/bash 

. ~/.colors.sh

find_git_dirty() {
    local status=$(git status --porcelain 2> /dev/null)
    if [[ "$status" != "" ]]; then
        return 1
    fi
    return 0
}

echo "Searching git directories..."
dirs=$(find . -name .git)
for d in $dirs; do
    d=$(echo $d | sed 's/\.git//')
    (\
        echo -n $d; \
        cd $d; \
        (git checkout master && git pull origin master || git pull origin develop) > /dev/null 2>&1; \
        find_git_dirty || echo -n " $txtred*$txtrst"; \
        echo; \
    )
done

