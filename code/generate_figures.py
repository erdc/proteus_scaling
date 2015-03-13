import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = 10, 8

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
    fig, axes = plt.subplots(nrows=2, sharex=True, sharey=True)
    f = open('results/marin_proteus_asm_log.txt')
    residuals, asm_walltimes = parse_log(f)
    plot_residuals(axes[0], residuals, asm_walltimes)
    axes[0].set_title('Proteus ASM');
    f = open('results/marin_fieldsplit_asm_log.txt')
    residuals, fs_walltimes = parse_log(f)
    plot_residuals(axes[1], residuals, fs_walltimes)
    axes[1].set_title('Proteus FieldSplit')
    axes[1].set_xlabel('Walltime')
    plt.savefig('figures/marin_comparison.png')

if __name__ == '__main__':
    plot_plunging()
    plot_marin()