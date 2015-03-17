import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 10, 8

refinements = [32, 64, 96, 128]
solvers = ['test_proteus_asm', 
           'test_fieldsplit_3D_schur_full_asm', 
           'test_fieldsplit_3D_schur_upper_asm', 
           'test_fieldsplit_3D_schur_diag_asm']
names = ['Proteus ASM', 'Schur - Full', 'Schur - Upper', 'Schur - Diag']

def parse_log(f):
    residuals = []
    walltimes = []
    line = f.readline()
    while not line.startswith('***'):
        if line.startswith('Stage:'):
            idx = int(line.partition('_p_L_')[2].split('_')[0])
            line = f.readline()
            this_residuals = []
            while not (line.startswith('***') or line.startswith('Stage:')):
                if 'true resid norm' in line and not line.startswith('    '):
                    this_residuals.append(float(line.partition('true resid norm ')[2].split()[0]))
                line = f.readline()
            residuals.append((idx, this_residuals))
        else:
            line = f.readline()
    while not line.startswith('Summary of Stages:'): 
        line = f.readline()
    ignore = f.readline(), f.readline()
    line = f.readline()
    while not line.startswith('\n'):
        idx = int(line.partition('_p_L_')[2].split('_')[0])
        walltime = float(line.split(':')[2].split()[0])
        walltimes.append((idx, walltime))
        line = f.readline()
    return sorted(residuals), sorted(walltimes)

def get_residual_stats(f):
    residuals, walltimes = parse_log(f)
    residuals = [len(r[1]) for r in residuals]
    min_r, max_r, mean_r = min(residuals), max(residuals), np.mean(residuals)
    return min_r, max_r, mean_r

def get_walltime_stats(f):
    residuals, walltimes = parse_log(f)
    walltimes = [w[1] for w in walltimes]
    min_w, max_w, mean_w = min(walltimes), max(walltimes), np.mean(walltimes)
    return min_w, max_w, mean_w

def get_weak_scale(solver, refinements, stats):
    solver_mins = []
    solver_maxs = []
    solver_means = []
    for r in refinements:
        result = 'results/' + solver + '_' + str(r) + '.txt'
        f = open(result)
        min_w, max_w, mean_w = stats(f)
        solver_mins.append(min_w)
        solver_maxs.append(max_w)
        solver_means.append(mean_w)
    return solver_mins, solver_maxs, solver_means

def plot_weak_time_study(solvers, refinements, names):
    fig, axes = plt.subplots(nrows=3, sharex=True)
    axes[0].set_title('Minimum Time')
    axes[1].set_title('Maximum Time')
    axes[2].set_title('Mean Time')
    for solver in solvers:
        mins, maxs, means = get_weak_scale(solver, refinements, stats=get_walltime_stats)
        axes[0].plot(mins, 'x:')
        axes[1].plot(maxs, 'x:')
        axes[2].plot(means, 'x:')
    for a in axes:
        a.set_xlim(-0.2, 3.2)
    axes[0].legend(names, loc='best')
    plt.xticks([0, 1, 2, 3], refinements)
    plt.savefig('figures/marin_time_scalability.png')

def plot_weak_iteration_study(solvers, refinements, names):
    fig, axes = plt.subplots(nrows=3, sharex=True)
    axes[0].set_title('Minimum Krylov Iterations')
    axes[1].set_title('Maximum Krylov Iterations')
    axes[2].set_title('Mean Krylov Iterations')
    for solver in solvers:
        mins, maxs, means = get_weak_scale(solver, refinements, stats=get_residual_stats)
        axes[0].plot(mins, 'x:')
        axes[1].plot(maxs, 'x:')
        axes[2].plot(means, 'x:')
    for a in axes:
        a.set_xlim(-0.2, 3.2)
    axes[0].legend(names, loc='best')
    plt.xticks([0, 1, 2, 3], refinements)
    plt.savefig('figures/marin_iterations_scalability.png')

def plot_residuals(ax, residuals, walltimes):
    for (idx1, i_residuals), (idx2, walltime) in zip(residuals, walltimes):
        assert idx1 == idx2
        residual_times = np.linspace(0, walltime, len(i_residuals))
        ax.semilogy(residual_times, i_residuals, ':.', markersize=4)
    ax.set_ylabel('True residual error')
    ax.grid(True)

def plot_plunging():
    fig, axes = plt.subplots(nrows=2, sharex=True, sharey=True)
    f = open('results/plunging_asm_log.txt')
    residuals, asm_walltimes = parse_log(f)
    plot_residuals(axes[0], residuals, asm_walltimes)
    axes[0].set_title('Proteus ASM');
    f = open('results/plunging_fieldsplit_asm_log.txt')
    residuals, fs_walltimes = parse_log(f)
    plot_residuals(axes[1], residuals, fs_walltimes)
    axes[1].set_title('Proteus FieldSplit')
    axes[1].set_xlabel('Walltime')
    plt.savefig('figures/plunging_comparison.png')

def plot_marin():
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True)
    f = open('results/test_proteus_asm_128.txt')
    residuals, asm_walltimes = parse_log(f)
    plot_residuals(axes[0], residuals, asm_walltimes)
    axes[0].set_title('Proteus ASM');
    f = open('results/test_fieldsplit_3D_schur_upper_asm_128.txt')
    residuals, fs_walltimes = parse_log(f)
    plot_residuals(axes[1], residuals, fs_walltimes)
    axes[1].set_title('Schur Complement (Upper)')
    f = open('results/test_fieldsplit_3D_schur_full_asm_128.txt')
    residuals, fs_walltimes = parse_log(f)
    plot_residuals(axes[2], residuals, fs_walltimes)
    axes[2].set_title('Schur Complement (Full)')
    axes[2].set_xlabel('Walltime')
    axes[2].set_xlim(0, 20)
    plt.savefig('figures/marin_comparison.png')

if __name__ == '__main__':
    plot_plunging()
    plot_marin()
    plot_weak_time_study(solvers, refinements, names)
    plot_weak_iteration_study(solvers, refinements, names)



