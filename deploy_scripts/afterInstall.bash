#!/usr/bin/env bash

rsync --delete-before --verbose --archive /home/django/envs/dashboard/release/ /home/django/envs/dashboard/talentstomorrow/ > /var/log/deploy.log