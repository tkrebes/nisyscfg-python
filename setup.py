import os
from setuptools import find_packages
from setuptools import setup


pypi_name = "nisyscfg"


def read_contents(file_to_read):
    with open(file_to_read, "r") as f:
        return f.read()


def get_version():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    version_path = os.path.join(script_dir, pypi_name, "VERSION")
    return read_contents(version_path).strip()


setup(
    name=pypi_name,
    zip_safe=True,
    version=get_version(),
    description="NI System Configuration Python API",
    long_description=read_contents("README.rst"),
    long_description_content_type="text/x-rst",
    author="National Instruments",
    url="https://github.com/tkrebes/nisyscfg-python",
    maintainer="Tyler Krehbiel",
    maintainer_email="tyler.krehbiel@ni.com",
    keywords=[pypi_name, "syscfg"],
    license="MIT",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "hightime",
        "six",
    ],
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Hardware :: Hardware Drivers",
    ],
    package_data={pypi_name: ["VERSION"]},
)
