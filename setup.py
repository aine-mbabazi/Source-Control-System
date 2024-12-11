# Setup script for installation
from setuptools import setup, find_packages

setup(
    name='trina',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trina=trina:main',
        ],
    },
    description='A distributed source control system',
    long_description='Trina is a simple, Git-like version control system',
    author='Your Name',
    author_email='patainembabazi@gmail.com',
    url='https://github.com/aine-mbabazi/Source-Control-System',
)