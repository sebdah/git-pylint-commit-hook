""" Setup script for PyPI """
from setuptools import setup

setup(
    name='git-pylint-commit-hook',
    version='2.0.2',
    license='Apache License, Version 2.0',
    description='Git commit hook that checks Python files with pylint',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='http://www.sebastiandahlgren.se',
    keywords="git commit pre-commit hook pylint python",
    platforms=['Any'],
    packages=['git_pylint_commit_hook'],
    scripts=['git-pylint-commit-hook'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
