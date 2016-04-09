#!/usr/bin/env bash

# I have left a few things in here and will explain this further (see below)
rsync --delete-before --verbose --archive /home/django/envs/dashboard/release/ /home/django/envs/dashboard/talentstomorrow/ > /var/log/deploy.log