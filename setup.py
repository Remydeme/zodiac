"""zodiac package is used to fetch gmail mail, analyse them using mchine learning
and exploit the result.
"""

from io import open
from os import path

from setuptools import setup
THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='zodiac',
    version='1.0.0rc5',
    description='A Mails analyser tools',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/Remydeme/zodiac-sutime',
    author='DEME Rémy',
    author_email='demeremy@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='Ocoto mail analyser',
    packages=['zodiac'],
    install_requires=[
        'JPype1>=0.6.0',
        'pandas',
        'numpy',
        'sklearn',
        'zodiac_sutime',
        'skmultilearn',
        'google-api-core',
        'google-api-python-client',
        'google-auth',
        'zodiac_sutime'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'unittest',
        'pytest',
        'python-dateutil'
    ],
    package_data={
        'zodiac_sutime': [
            'jars/stanford-corenlp-sutime-python-1.4.0.jar',
            'stanford-corenlp-3.9.2-models-french.jar'
        ],
    },
    package_dir={'zodiac': 'zodiac'},
    include_package_data=True,
    zip_safe=False
)
