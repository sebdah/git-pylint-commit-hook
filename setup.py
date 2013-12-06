""" Setup script for PyPI """
import os
from setuptools import setup
from ConfigParser import SafeConfigParser

settings = SafeConfigParser()
settings.read(os.path.realpath('lib/settings.conf'))


setup(
    name='git-pylint-commit-hook',
    version=settings.get('general', 'version'),
    license='Proprietary',
    description='Git commit hook that checks Python files with pylint',
    author='Sebastian Dahlgren',
    author_email='sebastian.dahlgren@gmail.com',
    url='http://www.sebastiandahlgren.se',
    keywords="git commit pre-commit hook pylint python",
    platforms=['Any'],
    packages=['lib'],
    scripts=['cumulus'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)
