import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ponzi',
    version='0.1',
    packages=['ponzi'],
    install_requires=['django', 'bitcoin-python'],
    include_package_data=True,
    license='BSD License',
    description='A cryptocurrency ponzi app for Django.',
    long_description=README,
    url='https://github.com/realspencerdupre/django-ponzi',
    author='Spencer Dupre',
    author_email='spencer.dupre@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
