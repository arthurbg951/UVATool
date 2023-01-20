from setuptools import setup, find_packages

lib_path = f'{__file__[:-12]}libs'

pkg_names = ['UVATool', 'UVATool/Enums', 'UVATool/Exceptions']
lib_folders = []
for pkg_name in pkg_names:
    lib_folders.append(f'{lib_path}/{pkg_name}')

pkg_dir = {}
for i in range(len(pkg_names)):
    pkg_dir[pkg_names[i]] = lib_folders[i]

setup(
    name='UVATool',
    version='1.0.0',
    author='Arthur Brito',
    author_email='arthurbg951@hotmail.com',
    description='Simula estruturas reticuladas utilizando MNE ou MRA',
    packages=pkg_names,
    package_dir=pkg_dir,
    classifiers=[
        'Programming Language :: Python :: 3',
            'Licence :: GPL-2.0',
            'Operating System :: OS Independent'
    ],
    requires=['numpy']
)
