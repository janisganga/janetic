from setuptools import setup, find_packages

setup(
    name='janetic',
    version='0.1.0',
    description='A Python library for genetic algorithms',
    author='Janis Ganga',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy'
    ],
    entry_points={}
)