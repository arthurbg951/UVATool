from setuptools import setup, find_packages

setup(
    name='UVATool',
    version='1.0',
    author='Arthur Brito',
    author_email='arthurbg951@hotmail.com',
    description='Simula estruturas reticuladas utilizando MNE ou MRA',
    packages=[
        'UVATool',
        'UVATool/Enums',
        'UVATool/Exceptions'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Licence :: GPL-2.0',
        'Operating System :: OS Independent'
    ],
    requires=['numpy']
)
