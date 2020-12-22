import os

from setuptools import setup, find_packages


def read(fname: str):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hosts_editor",
    version="1.0.0",
    author="Ethan Wass",
    author_email="eitanwass@gmail.com",
    description="A simple API for editing the hosts file.",
    license="BSD",
    keywords="hosts file editing api",
    url="",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=read('requirements.txt').splitlines()
)
