#!/bin/bash -xe
#Source: https://sigmoidal.io/automatic-code-quality-checks-with-git-hooks/

echo "Running pre-commit hook"
./scripts/linter.sh

# $? stores exit value of the last command
if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi