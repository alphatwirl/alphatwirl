from setuptools import setup, find_packages
import os
import versioneer
import pypandoc

here = os.path.abspath(os.path.dirname(__file__))

long_description = pypandoc.convert('README.md', 'rst')

setup(
    name='alphatwirl',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A Python library for summarizing event data',
    long_description=long_description,
    author='Tai Sakuma',
    author_email='tai.sakuma@gmail.com',
    url='https://github.com/alphatwirl/alphatwirl',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'images', 'tests']),
)
