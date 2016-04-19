#!/usr/bin/env bash

if [ -d /home/django/envs/dashboard/ ]; then
    rm -rf /home/django/envs/dashboard/release
fi
mkdir -vp /home/django/envs/dashboard/release