from setuptools import setup, find_packages

with open("README.md") as file:
    long_desc = file.read()

setup(
    name="aioheleket",
    version="1.1.0",
    author="SuperFeda",
    description="Asynchronous Python library for Heleket",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3.10',
    url="https://github.com/SuperFeda/aioheleket",
    download_url="https://github.com/SuperFeda/aioheleket",
    packages=find_packages()
)
