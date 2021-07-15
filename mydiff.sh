# for git diff
sdiff --diff-program=colordiff --ignore-tab-expansion --ignore-trailing-space --ignore-all-space --ignore-blank-lines -w$(tput cols) "$2" "$5"
#colordiff "$2" "$5"
