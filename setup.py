import os

from setuptools import setup, find_packages


def read(fname: str):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hosts_editor",
    version="1.0.0",

    author="Ethan Wass",
    author_email="eitanwass@gmail.com",

    license="MIT",
    keywords="hosts file editing api",
    url="https://github.com/eitanwass/hosts_editor",
    packages=find_packages(),

    description="A simple API for editing the hosts file.",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",

    install_requires=read('requirements.txt').splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
