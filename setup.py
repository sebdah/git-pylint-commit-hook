""" Setup script for PyPI """
from setuptools import setup

setup(
    name='git-pylint-commit-hook',
    version='2.6.1',
    license='Apache License, Version 2.0',
    description='Git commit hook that checks Python files with pylint',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='https://github.com/sebdah/git-pylint-commit-hook',
    keywords="git commit pre-commit hook pylint python",
    platforms=['Any'],
    packages=['git_pylint_commit_hook'],
    scripts=['git-pylint-commit-hook'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pylint<2.7',
        'future'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <=3.6',
)
