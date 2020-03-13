#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='web-parsers',
    version='0.0.3',
    description='Convert HTML, XML, RDF data into JSON using YAML configurations '
                'and occasionally with pythonic functions',
    author='Ravi Raja Merugu',
    author_email='ravi@invanalabs.ai',
    url='https://github.com/invanalabs/web-parser',
    packages=find_packages(
        exclude=("dist", "docs", "tests",)
    ),
    install_requires=[
        'parsel>=1.5.2',
        'PyYAML==5.1.2'
        'xmltodict==0.12.0'
    ],
    entry_points={
    },
)
