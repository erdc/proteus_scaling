import os
import sys
from itertools import count

import petsc4py

petsc4py.init(sys.argv)

from petsc4py import PETSc

def convert_mat(data_file, name, block_size=3):
    viewer = PETSc.Viewer().createBinary(data_file, 'r')
    A, viewer = load_A_blocked(viewer, block_size)
    b = A.getVecLeft()
    b.load(viewer)

    out_viewer = PETSc.Viewer().createBinary(data_file + '_blocked_' + str(block_size), 'w')
    A.view(out_viewer)
    b.view(out_viewer)

def load_A_blocked(viewer, block_size=3):
    A = PETSc.Mat()
    A.create()
    A.setBlockSize(block_size)
    A.setFromOptions()
    A.load(viewer)
    return A, viewer

def iter_systems(file_list):
    for filename in file_list:
        if os.path.exists(filename):
            name = os.path.basename(filename)
            yield filename, name

block_size = int(sys.argv[1])

mat_files = [filename for filename in sys.argv[2:] if not (filename.endswith('.info') or filename.endswith('.options'))]

for file, name in iter_systems(mat_files):
    convert_mat(file, name)

def iter_systems(file_prefix, name_prefix):
    for i in count():
        filename = file_prefix + str(i)
        if os.path.exists(filename):
            yield filename, name_prefix + str(i)
        else:
            return

for file, name in iter_systems(file_prefix, name_prefix):
    convert_mat(file, name, block_size)

