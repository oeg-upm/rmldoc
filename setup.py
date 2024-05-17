# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

install_requires = [
    "rdflib>=6.0.2",
    "Jinja2>=3.1.2",
    "yatter>=1.1.2"
]


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]


setup(
    name="rmldoc",
    version="0.1.7",
    author="Jhon Toledo",
    author_email="ja.toledo@upm.es",
    description="Rmldoc is a tool that generates documentation of RML mappings",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/rmldoc",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    entry_points={"console_scripts": ["rmldoc = rmldoc.__main__:main"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["rmldoc.tests*"]),
    package_data={"rmldoc": find_package_data("src/rmldoc")},
    exclude_package_data={"rmldoc": ["test/*"]},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.8",
)
