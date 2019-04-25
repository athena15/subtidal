from setuptools import setup

__version__ = '1.0.1'
__author__ = 'Brenner Heintz'

description = "Subtidal, for batch downloading subtitles for all movies in a central media folder."

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    dependencies = f.read().splitlines()

setup(
    name="subtidal",
    version=__version__,
    author=__author__,
    author_email="brennerhdata@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/athena15/subtidal",
    include_package_data=True,
    packages=['subtidal'],
    py_modules=['subtidal'],
    entry_points='''
            [console_scripts]
            download-subtitles=subtidal.cli:download_subtitles
        ''',
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent"],
    install_requires=dependencies
)