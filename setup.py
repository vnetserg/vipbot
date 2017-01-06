#!/usr/bin/env python

import os
import pip
from setuptools import setup


# Parse requirements:
req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
requires = list(pip.req.parse_requirements(req_path, session=pip.download.PipSession()))

setup(
    name='vipbot',
    version='0.1.0',
    description='Telegram bot for reporting current IP address of machine',
    author='Sergei Fomin',
    author_email='sergio-dna@yandex.ru',
    install_requires=[str(r.req) for r in requires if r.req],
    dependency_links=[str(r.link) for r in requires if r.link],
    py_modules=['vipbot']
)
