from setuptools import setup, find_packages

with open("qleet/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

with open("requirements.txt") as f:
    requirements = list(map(lambda x: x.strip(), f.readlines()))

setup(
    name = "qleet",
    version = version,
    author = "Utkarsh Azad, Animesh Sinha",
    author_email = "utkarshazad98@gmail.com, animeshsinha.1309@gmail.com",
    maintainer = "QLemma",
    maintainer_email = "utkarshazad98@gmail.com",
    url = "https://github.com/QLemma/qleet",
    py_modules=['qleet'],
    license = "Apache License 2.0",
    packages = find_packages(),
    description = "qLEET is an open-source library for exploring Loss landscape, Expressibility, Entangling"
                  "capability and Training trajectories of noisy parameterized quantum circuits.",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    provides = ["qleet"],
    install_requires = requirements,
    package_data = {"qleet": ["tests/pytest.ini"]},
    include_package_data = True,
    classifiers = [
        "Development Status :: 4 - Beta",
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
)
