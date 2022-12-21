"""Packaging logic for emacs-vhdl-formatter."""

__author__ = "Thierry Delafontaine (deaa@zhaw.ch)"
__copyright__ = "2022 ZHAW Institute of Embedded Systems"
__date__ = "2022-12-20"

import codecs

from setuptools import find_packages, setup

with codecs.open("README.md", "r", "utf-8") as fd:
    setup(
        name="emacs-vhdl-formatter",
        version="1.0.0",
        description="Format your VHDL files with emacs",
        long_description=fd.read(),
        license="MIT",
        license_file="LICENSE",
        author="Thierry Delafontaine",
        author_email="deaa@zhaw.ch",
        maintainer="Thierry Delafontaine",
        maintainer_email="deaa@zhaw.ch",
        packages=find_packages("."),
        url="https://github.com/InES-HPMM/pre-commit-emacs-vhdl-formatter",
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Utilities",
        ],
        entry_points={
            "console_scripts": [
                "emacs-vhdl-formatter = "
                "pre_commit_hooks.emacs_vhdl_formatter:main",
            ],
        },
    )
