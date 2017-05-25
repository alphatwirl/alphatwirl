from setuptools import setup, find_packages

setup(
    name = 'AlphaTwirl',
    version= '0.9',
    description = 'A Python library for summarizing event data',
    author = 'Tai Sakuma',
    author_email = 'tai.sakuma@gmail.com',
    url = 'https://github.com/TaiSakuma/AlphaTwirl',
    packages = find_packages(exclude=['docs', 'images', 'tests']),
)
