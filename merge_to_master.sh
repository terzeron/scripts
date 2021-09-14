#!/bin/bash

echo "git switch develop"
git switch develop > /dev/null
echo "git push"
git push > /dev/null
echo "git switch master"
git switch master > /dev/null
echo "git merge develop"
git merge develop > /dev/null
echo "git push"
git push > /dev/null
echo "git switch develop"
git switch develop > /dev/null

