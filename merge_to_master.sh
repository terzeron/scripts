#!/bin/bash

echo "git switch develop"
git switch develop > /dev/null
echo "git stash"
git stash > /dev/null
echo "git push"
git push > /dev/null
echo "git switch master"
git switch master > /dev/null
echo "git pull"
git pull > /dev/null
echo "git merge develop"
git merge develop > /dev/null
echo "git push"
git push > /dev/null
echo "git switch develop"
git switch develop > /dev/null
echo "git stash pop"
git stash pop > /dev/null

