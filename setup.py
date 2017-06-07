from setuptools import setup, find_packages

setup(
    name = 'alphatwirl',
    version= '0.9.5',
    description = 'A Python library for summarizing event data',
    author = 'Tai Sakuma',
    author_email = 'tai.sakuma@gmail.com',
    url = 'https://github.com/alphatwirl/alphatwirl',
    packages = find_packages(exclude=['docs', 'images', 'tests']),
)
