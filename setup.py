#!/usr/bin/python3

import os
from setuptools import setup


def get_packages(base="chordinstability"):
    """Return all modules used in chord-instability."""
    if not os.path.exists(os.path.join(base, "__init__.py")):
        # only python modules
        return []

    result = [base.replace("/", ".")]
    for name in os.listdir(base):
        if not os.path.isdir(os.path.join(base, name)):
            continue

        if name == "__pycache__":
            continue

        # find more python submodules in that directory
        result += get_packages(os.path.join(base, name))

    return result


setup(
    name="chord-instability",
    version="0.0.1",
    description="Calculating instability of chords",
    author="Sezanzeb",
    author_email="proxima@sezanzeb.de",
    url="https://github.com/sezanzeb/chord-instability",
    license="MIT",
    packages=get_packages(),
    include_package_data=True,
    install_requires=["numpy"],
)
