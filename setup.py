#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='web-parsers',
    version='0.0.2',
    description='Simple, extendable HTML and XML data extraction engine using YAML configurations '
                'and some times pythonic functions.',
    author='Ravi Raja Merugu',
    author_email='ravi@invanalabs.ai',
    url='https://github.com/invanalabs/web_parsers',
    packages=find_packages(
        exclude=("dist", "docs", "tests",)
    ),
    install_requires=[
        'parsel>=1.5.2',
        'PyYAML>=5.3.1',
        'xmltodict==0.12.0'
    ],
    entry_points={
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
