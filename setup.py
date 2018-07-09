import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonjsc",
    version="1.0.0",
    author="C. Foster",
    author_email="korewananda@gmail.com",
    description="A package to parse out C/JS style block and single line comments from JSON files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NouberNou/jsonjsc",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)