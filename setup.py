from setuptools import setup, find_packages
import os, sys

required_pkgs = []

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Communications :: File Sharing",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="python-rtorrent",
    version='0.1.0',
    url='https://github.com/kinabcd/python-rtorrent',
    author='Kin Lo',
    author_email='kinabcd@gmail.com',
    maintainer='Kin Lo',
    maintainer_email='kinabcd@gmail.com',
    description='A rTorrent interface not required to run HTTP Server',
    keywords="rtorrent",
    license="GPL",
    packages=find_packages(),
    scripts=[],
    install_requires=required_pkgs,
    classifiers=classifiers,
    include_package_data=True,
)

