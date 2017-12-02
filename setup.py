from setuptools import setup, find_packages

setup(
    name = 'alphatwirl',
    version= '0.9.7',
    description = 'A Python library for summarizing event data',
    author = 'Tai Sakuma',
    author_email = 'tai.sakuma@gmail.com',
    url = 'https://github.com/alphatwirl/alphatwirl',
    packages = find_packages(exclude=['docs', 'images', 'tests']),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
