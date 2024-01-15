#!/bin/bash

source ~/.colors.sh

main_branch=$(git branch -l | sed -n -E 's/ +(main|master)$/\1/ p')

echo "git switch ${bldpur}develop${txtrst}"
git switch develop > /dev/null
echo "git stash"
git stash > /dev/null
echo "git push"
git push > /dev/null
echo "git switch ${bldred}${main_branch}${txtrst}"
git switch "$main_branch" > /dev/null
echo "git pull"
git pull > /dev/null
echo "git merge develop"
git merge develop > /dev/null
echo "git push"
git push > /dev/null
echo "git switch ${bldpur}develop${txtrst}"
git switch develop > /dev/null
echo "git stash pop"
git stash pop > /dev/null

