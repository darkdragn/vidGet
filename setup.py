#!/usr/bin/env python

from setuptools import setup

VERSION = (0, 1)
VERSION_STR = ".".join([str(x) for x in VERSION])

setup(
    name='vidGet',
    version=VERSION_STR,
    description="Video streaming site ripping tool.",
    license='BSD',
    # long_description=open('README.rst', 'r').read(),
    author='Christopher Jackson',
    author_email='darkdragn.cj@gmail.com',
    url='https://github.com/darkdragn/vidGet',
    packages=['vidGet', 'vidGet.sites'],
    scripts=['vidGetCli'],
    install_requires=[
        'beautifulsoup4',
        'mechanize'
    ],
    # setup_requires=["nose>=1.0"],
    # test_suite = "nose.collector",
    keywords=['anime', 'cartoons', 'streaming'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
