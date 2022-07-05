#!/usr/bin/python

import glob
import os

def sortByNameWithExtension(extension):
    files = glob.glob(extension)
    files.sort(key=os.path.abspath)
    return files