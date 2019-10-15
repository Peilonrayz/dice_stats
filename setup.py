#!/usr/bin/env python

"""setup.py."""

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='dice_stats',
    version='1.0.0',
    license='MIT',
    description='Get statistics for rolling dice.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Peilonrayz',
    author_email='peilonrayz@gmail.com',
    url='https://github.com/Peilonrayz/dice_stats',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    keywords='dice statistics simulation',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'numpy',
    ],
    extras_require={
        'dev':  [
            'tox',
        ]
    },
)
