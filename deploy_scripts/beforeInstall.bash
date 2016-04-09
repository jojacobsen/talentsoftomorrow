#!/usr/bin/env bash

# I want to make sure that the directory is clean and has nothing left over from
# previous deployments. The servers auto scale so the directory may or may not
# exist.
if [ -d /home/django/envs/dashboard/ ]; then
    rm -rf /home/django/envs/dashboard/release
fi
mkdir -vp /home/django/envs/dashboard/release