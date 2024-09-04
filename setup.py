from setuptools import setup, find_packages

# from my_pip_package import __version__

setup(
    name='my_pip_package',
    version='dev',

    url='https://github.com/guialba/rlenvs',
    author='Guiulherme Albarrans Leite',
    # author_email='mkim0407@gmail.com',

    # py_modules=['my_pip_package'],
    packages=find_packages()
)