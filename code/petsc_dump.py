"""
Helper module for extracting PETSc systems of equations from Proteus

Put this file in the same directory as your application
Edit it to your needs
Use this patch to enable the petsc_dump hooks: https://github.com/erdc-cm/proteus/commit/e7b475dea376a4100949aa807682d3192f344170
"""

from petsc4py import PETSc
import json
import sys
import os

from proteus import version
import subprocess

app_name = 'Ubbink_coarse'
app_version = subprocess.check_output(version.git_cmd, cwd=os.path.dirname(__file__)).strip()

times = [0.0, 0.01, 0.02]
models = ['twp_navier_stokes_p', 'vof_p']

meta = {'name': app_name,
        'models': models,
        'resolution': 'unknown'
        'sizes': 'unknown',
        'url': 'https://github.com/erdc-cm/air-water-vv/tree/master/2d/dambreak_Ubbink',
        'versions': {'hashdist': version.hashdist,
                     'hashstack': version.hashstack,
                     'proteus': version.proteus,
                     'proteus-mprans': 'unknown',
                     'app': app_version},
        'argv': sys.argv,
        'dim': 2,
        'times': times}

ns = None
time_idx = 0
ready_models = models[:]

meta_name = app_name + '.json'
active_model = None

def meta_dump():
    with open(meta_name, 'w') as f:
        json.dump(meta, f, indent=4)

def petsc_dump(A, u, b):
    global time_idx
    global ready_models

    if active_model.name not in ready_models or time_idx >= len(times) or ns.tn <= times[time_idx]:
        return

    system_name = app_name + '_' + active_model.name + '_L_%d' % time_idx
    system_file = PETSc.Viewer().createBinary(system_name, comm=PETSc.COMM_WORLD, mode=PETSc.Viewer.Mode.WRITE)
    A.view(system_file)
    b.view(system_file)
    u.view(system_file)

    ready_models.remove(active_model.name)

    if not ready_models:
        time_idx += 1
        ready_models = models[:]
