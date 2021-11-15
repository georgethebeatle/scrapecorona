"""Setup the project."""
from setuptools import setup, find_packages


setup(
    name='scrapecorona',
    version='0.1',
    packages=find_packages(),
    install_requires=['scrapy>=2.5.0', 'dateparser>=1.1.0'],
)


