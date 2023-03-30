# building our ml project as a package so anybody can install it.
# script that keeps the information regarding the packaging --version, author
from setuptools import find_packages,setup 
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filepath:str)->List[str]:
    # this function returns the list of requirements
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements

setup(
    name = 'mlend-end',
    version= '0.0.1',
    author='rahul',
    author_email='jrspatel12@gmail.com',
    packages=find_packages(),
    # it will see in how many folders we have the __init__.py file
    install_requires= get_requirements('requirements.txt')
)