from setuptools import setup, find_packages
import rlenvs

setup(
    name='rlenvs',
    version=rlenvs.__version__,

    url='https://github.com/guialba/rlenvs',
    author='Guiulherme Albarrans Leite',

    install_requires=[
        'numpy',
    ],
    packages=find_packages()
    
)