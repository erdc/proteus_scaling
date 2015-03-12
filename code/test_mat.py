import os
import sys
from itertools import count

import petsc4py

petsc4py.init(sys.argv)

from petsc4py import PETSc

def test_mat(data_file, name):
    viewer = PETSc.Viewer().createBinary(data_file, 'r')

    A, viewer = load_A_blocked(viewer)
    b = A.getVecLeft()
    b.load(viewer)
    x = A.getVecRight()
    PETSc.Sys.Print('Stage: ' + name)
    stage = PETSc.Log.Stage(name)
    stage.push()
    ksp = PETSc.KSP()
    ksp.create(PETSc.COMM_WORLD)
    ksp.setOperators(A)
    ksp.setFromOptions()
    ksp.solve(b, x)
    stage.pop()
    A.destroy()
    ksp.destroy()
    x.destroy()
    b.destroy()

def load_A_blocked(viewer):
    A = PETSc.Mat()
    A.create()
    A.setBlockSize(3)
    A.setFromOptions()
    A.load(viewer)
    return A, viewer

def load_A(data_file, viewer):
    # number of fields, is f
    f = 3
    A = PETSc.Mat().load(viewer)
    # Let's load it twice like idiots
    (m, M), (n, N) = A.getSizes()

    viewer = PETSc.Viewer().createBinary(data_file, 'r')
    A = PETSc.Mat()
    A.create()

    A.setSizes(((m, n), (M*f, N*f)))

    A.setFromOptions()
    A.load(viewer)
    return A, viewer

data_file = '/Users/aron/adwr/input/liquid_column_collapse/liquid_column_collapse_twp_navier_stokes_p_L_0'

name_prefix = 'liquid_column_collapse_twp_navier_stokes_p_L_'
file_prefix = '/Users/aron/adwr/input/liquid_column_collapse/liquid_column_collapse_twp_navier_stokes_p_L_'

def iter_systems(file_prefix, name_prefix):
    for i in count():
        filename = file_prefix + str(i) + '_blocked_3'
        if os.path.exists(filename):
            yield filename, name_prefix + str(i)
        else:
            return

for file, name in iter_systems(file_prefix, name_prefix):
    test_mat(file, name)

