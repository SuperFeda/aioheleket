from setuptools import setup, find_packages

with open("./README.md") as file:
    long_desc = file.read()

setup(
    name="aioheleket",
    version="1.2.0",
    author="SuperFeda",
    description="Asyncio Python library for Heleket crypto payments",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3.10',
    url="https://github.com/SuperFeda/aioheleket",
    download_url="https://pypi.org/project/aioheleket/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=[
        "heleket",
        "heleketapi",
        "asyncio",
        "api",
        "crypto",
        "cryptocurrency",
        "cryptopayments"
    ],
    packages=find_packages()
)
