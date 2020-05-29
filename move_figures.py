#!/usr/bin/env python3

"""
Move figures to the end of the file.
"""

import sys
import os
import re
import bs4

import subprocess
from subprocess import PIPE


if len(sys.argv) != 2:
    print("Usage: move_figures.py document.tex")
    sys.exit(0)

tex_file = sys.argv[1]

with open(tex_file, 'rb') as f:
    data = f.read().decode('utf-8')

regexp = re.compile(r'(\\begin\{figure[*]?}.*?\\end\{figure[*]?})',
                    re.DOTALL|re.MULTILINE)

figures = re.findall(regexp, data)
data = re.sub(regexp, '', data)
data = data.replace('%% FIGURES HERE %%', '\n\n'.join(figures))

with open(tex_file, 'w') as f:
    f.write(data)
