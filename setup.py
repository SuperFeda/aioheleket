from setuptools import setup, find_packages

setup(
    name="aioheleket",
    version="1.0.0",
    author="SuperFeda",
    description="Asynchronous Python library for Heleket",
    long_description=open("README.md").read(),
    license=open("LICENSE").read(),
    python_requires='>=3.10',
    url="https://github.com/SuperFeda/aioheleket",
    packages=find_packages()
)
