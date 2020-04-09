import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ['BIRD']

requires = []

setuptools.setup(
    name='BIRDpy',
    version='2020.4.1',
    install_requires=requires,
    author="D. van Gorkum",
    author_email="djvg@djvg.net",
    description="Python 3 module to talk to BIRD control socket.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDJVG/BIRDpy",
    python_requires='>=3.6',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)