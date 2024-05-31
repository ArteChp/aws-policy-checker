# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='AWS Policy Checker',
    version='0.1.0',
    description='AWS Policy Checker for Globant',
    long_description=readme,
    author='Arte Chp',
    author_email='art.cha@tutanota.com',
    url='https://github.com/ArteChp/aws_policy_checker',
    packages=find_packages(exclude=('tests', 'docs'))
)

