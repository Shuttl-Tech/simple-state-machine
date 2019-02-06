from setuptools import setup, find_packages

setup(
    name="simple_state_machine",
    version="0.1",
    description="Utilities",
    url="https://github.com/Shuttl-Tech/simple-state-machine",
    author="Dhruv Agarwal",
    author_email="dhruv.agarwal@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=[],
    extras_require={
        "test": ["pytest"],
    },
)