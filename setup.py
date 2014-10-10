#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='filerooms',
    version='0.0.1',
    url='https://github.com/snowball-one/filerooms',
    author="Jonathan Moss",
    author_email="jmoss@snowballone.com.au",
    description="a private/public file manager for django",
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('CHANGELOG.rst').read(),
    ]),
    keywords="django, file, private access",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'djangorestframework>=2.4.3',
        'django-sendfile>=0.3.6',
        'django-braces>=1.4.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
    ]
)
