"""Setup the project."""
from setuptools import setup, find_packages


setup(
    name='scrapecorona',
    version='0.1',
    packages=find_packages(),
    install_requires=['scrapy>=2.5.0',
                      'dateparser>=1.1.0',
                      'notebook>=6.4.5',
                      'numpy>=1.21.4',
                      'pandas>=1.3.4',
                      'matplotlib>=3.4.3'],
)
