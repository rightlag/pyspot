import os
import pyspot

from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyspot',
    version=pyspot.__version__,
    description='A Python SDK used to interface with the Spotify Web API',
    long_description=long_description,
    url='https://github.com/rightlag/pyspot',
    author=pyspot.__author__,
    author_email='rightlag@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
    keywords='spotify web-api sdk',
    packages=find_packages(exclude=['test*'])
)
