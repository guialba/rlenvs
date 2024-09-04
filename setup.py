from setuptools import setup, find_packages

setup(
    name='rlenvs',
    version=0.1,

    url='https://github.com/guialba/rlenvs',
    author='Guiulherme Albarrans Leite',

    install_requires=[
        'numpy',
    ],
    packages=find_packages()
    
)