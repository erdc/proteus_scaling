import os
import sys
from itertools import count

import petsc4py

petsc4py.init(sys.argv)

from petsc4py import PETSc

def convert_mat(data_file, name):
    viewer = PETSc.Viewer().createBinary(data_file, 'r')
    A, viewer = load_A_blocked(viewer)
    b = A.getVecLeft()
    b.load(viewer)

    out_viewer = PETSc.Viewer().createBinary(data_file + '_blocked_3', 'w')
    A.view(out_viewer)
    b.view(out_viewer)

def load_A_blocked(viewer):
    A = PETSc.Mat()
    A.create()
    A.setBlockSize(3)
    A.setFromOptions()
    A.load(viewer)
    return A, viewer

name_prefix = 'plunging_breakers_twp_navier_stokes_p_L_'
file_prefix = '/home/aron/adwr-nearshore-hydro/input/plunging-breakers/plunging_breakers_twp_navier_stokes_p_L_'

def iter_systems(file_prefix, name_prefix):
    for i in count():
        filename = file_prefix + str(i)
        if os.path.exists(filename):
            yield filename, name_prefix + str(i)
        else:
            return

for file, name in iter_systems(file_prefix, name_prefix):
    convert_mat(file, name)

