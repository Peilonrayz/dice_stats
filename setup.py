#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="dice_stats",
    version="1.0.0",
    license="MIT",
    description="Get statistics for rolling dice.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    author="Peilonrayz",
    author_email="peilonrayz@gmail.com",
    url="https://peilonrayz.github.io/dice_stats",
    project_urls={
        "Bug Tracker": "https://github.com/Peilonrayz/dice_stats/issues",
        "Documentation": "https://peilonrayz.github.io/dice_stats",
        "Source Code": "https://github.com/Peilonrayz/dice_stats",
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="",
    # entry_points={"console_scripts": ["dice_stats=dice_stats.__main__:main"]},
)
