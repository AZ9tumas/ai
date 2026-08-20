import matplotlib.pyplot as plt
import matplotx
import numpy as np
plt.style.use(matplotx.styles.ayu['dark'])
#plt.style.use(matplotx.styles.ayu['light'])

%config InlineBackend.figure_format = 'svg'

# 2. Apply global 2K+ quality and modern styling configurations
plt.rcParams.update({
    # Resolution & Layout
    'figure.dpi': 150,                # High-res screen preview
    'savefig.dpi': 300,               # 300+ DPI for pristine 2K/4K saved images
    'savefig.bbox': 'tight',          # Automatically prevents clipped labels
    'savefig.transparent': True,       # Clean transparent backgrounds
    'figure.autolayout': True,        # Prevents overlapping text elements
    
    # Typography
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    
    # Clean Aesthetics (Removes harsh blacks and messy lines)
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'axes.edgecolor': '#cccccc',     # Light subtle borders
    'axes.linewidth': 0.8,
    'grid.color': "#1A1A1A",          # Very faint grid lines
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    
    # Remove top and right borders globally
    'axes.spines.top': False,
    'axes.spines.right': False,
})

def beautifulArray(n):
    start = [1]
    op = 0

    def update():
        nonlocal start, op
        temp = []

        for e in start:
            op += 1
            if 2 * e - 1 <= n:
                temp.append(2 * e - 1)

        for e in start:
            op += 1
            if 2 * e <= n:
                temp.append(2 * e)

        start = temp

    while len(start) < n:
        update()
    return op


n_values = []
op_values = []

for i in range(1, 11):
    n_values.append(i)
    op_values.append(beautifulArray(i))

n_values = np.array(n_values)
op_values = np.array(op_values)

# Plotting op vs n
plt.figure(figsize=(8, 5))
plt.plot(n_values, op_values, marker = 'o', linestyle='-', linewidth=2, label = "op(n)")
plt.plot(n_values, n_values, marker = 'o', linestyle='-', linewidth=2, label = "linear")
plt.plot(n_values, n_values ** 2, marker = 'o', linestyle='-', linewidth=2, label = "quadratic")
plt.plot(n_values, np.log(n_values), marker = 'o', linestyle = '-', linewidth = 2, label = "log")
plt.title('Operations (op) vs Array Size (n)')
plt.xlabel('n')
plt.ylabel('op')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(n_values)
plt.legend()
#plt.tight_layout()
plt.show()
