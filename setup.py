from setuptools import setup, find_packages

with open("qleet/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

requirements = [
    "cirq==0.11.0",
    "tensorflow_quantum==0.5.1",
    "tensorflow==2.4.1",
    "qiskit==0.26.2",
]

info = {
    "name": "qLEET",
    "version": version,
    "maintainer": "QLemma",
    "maintainer_email": "utkarshazad98@gmail.com",
    "url": "https://github.com/QLemma/qLEET",
    "license": "Apache License 2.0",
    "packages": find_packages(where="."),
    "entry_points": {"console_scripts": ["qleet-test=qleet.tests:cli"]},
    "description": "qLEET is an open-source library for exploring Loss landscape, Expressibility, Entangling capability and Training trajectories of noisy parameterized quantum circuits.",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "provides": ["qleet"],
    "install_requires": requirements,
    "package_data": {"qleet": ["tests/pytest.ini"]},
    "include_package_data": True,
}

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering :: Physics",
]

setup(classifiers=classifiers, **(info))
