# Copyright (C) 2024 RidgeRun, LLC (http://www.ridgerun.com)
# All Rights Reserved.
#
# The contents of this software are proprietary and confidential to RidgeRun,
# LLC.  No part of this program may be photocopied, reproduced or translated
# into another programming language without prior written consent of
# RidgeRun, LLC.  The user is free to modify the source code after obtaining
# a software license from RidgeRun.  All source code changes must be provided
# back to RidgeRun without any encumbrance.

# Install with: python3 -m pip install .
# For developer mode install with: python3 setup.py develop --user.

# pylint: skip-file


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="rrms_utils",
    version="1.2.0",
    author='RidgeRun LLC',
    author_email='support@ridgerun.com',
    description="RidgeRun Microservices Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://ridgerun.com',
    packages=setuptools.find_packages(),
    python_requires='>=3.0, <4',
    install_requires=[
        'sphinx',
        'sphinx_rtd_theme',
        'pydantic',
        'redis',
        'influxdb',
        'influxdb-client'
    ],
)
