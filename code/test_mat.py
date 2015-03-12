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

def iter_systems(file_list):
    for filename in file_list:
        if os.path.exists(filename):
            name = os.path.basename(filename)
            yield filename, name

mat_files = [filename for filename in sys.argv[1:] if not (filename.endswith('.info') or filename.endswith('.options'))]

for file, name in iter_systems(mat_files):
    test_mat(file, name)

