#!/usr/bin/env bash

rsync --delete-before --verbose --archive --exclude=dashboard/media /home/django/envs/dashboard/release/ /home/django/envs/dashboard/talentstomorrow/ > /var/log/deploy.log
chown -R django:django /home/django/envs/dashboard/talentstomorrow