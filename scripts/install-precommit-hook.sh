#!/bin/bash -xe
#Source: https://sigmoidal.io/automatic-code-quality-checks-with-git-hooks/

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
# this command creates symlink to our pre-commit script
ln -s ../../scripts/pre-commit.sh $GIT_DIR/hooks/pre-commit
echo "Done!"