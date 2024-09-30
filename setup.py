from setuptools import setup, find_packages
# import rlenvs

setup(
    name='rlenvs',
    # version=rlenvs.__version__,
    version=0.2.,
    url='https://github.com/guialba/rlenvs',
    author='Guiulherme Albarrans Leite',
    install_requires=[
        'numpy',
        'gymnasium',
        'pygame',
    ],
    packages=find_packages()
)