from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *


def build(version=None):
    with open('VERSION', 'r') as fh:
        bn = int(fh.read())
        bn += 1

    print('Building version {}'.format(bn))

    if version:
        bn += ",{}".format(version)

    local('docker build -t 468125874400.dkr.ecr.eu-central-1.amazonaws.com/api:0.{} .'.format(bn))

    with open('VERSION', 'w') as fh:
        fh.write(str(bn))


def push():
    with open('VERSION', 'r') as fh:
        bn = int(fh.read())

    print('Pushing version {}'.format(bn))

    local('docker push 468125874400.dkr.ecr.eu-central-1.amazonaws.com/api:0.{}'.format(bn))


def bp():
    build()
    push()
