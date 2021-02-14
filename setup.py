# coding: utf-8

from setuptools import setup, find_packages

    
setup(
    name='lambda-sqs-test',
    version='1.0',
    description='Testing lambda sqs throttlin behavior',
    author='Galen Dunkleberger',
    license='ASL',
    zip_safe=False,
    include_package_data=True,
    package_dir={"": "source"},
    packages=find_packages("source"),
    test_suite='tests'
)
