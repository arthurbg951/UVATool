# This is not the main UVATool Toolkit, check in src/libs/UVATool.py file
import os, sys

p = os.path.abspath('..\..\src\libs')
sys.path.insert(1, p)

from UVATool import *