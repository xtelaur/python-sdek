#!/usr/bin/env python

# coding: utf-8

import os
import sys

import cdek

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = []

setup(
    name='python-sdek',
    version=cdek.__version__,
    url='https://github.com/xtelaur/python-cdek.git',
    author='Alexander Gritsenko',
    author_email='echion@ya.ru',
    description='Python interface for CDEK APIs. http://www.cdek.ru',
    keywords='E-commerce, Delivery service, API',
    license='MIT License',
    packages=['cdek'],
    include_package_data=True,
    package_dir={'cdek': 'cdek'},
    install_requires=requirements,
    zip_safe=False,
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ]
)
