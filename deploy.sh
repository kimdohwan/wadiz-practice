#!/usr/bin/env bash

git add --all

git add -f .secrets/

eb deploy --profile eb-docker-deploy --staged

git reset HEAD .secrets/

git reset

eb open