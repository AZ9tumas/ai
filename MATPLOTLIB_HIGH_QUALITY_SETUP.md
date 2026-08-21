# Permanent High-Quality Matplotlib Setup

Configured on 2026-08-20 for user-wide use on macOS with Python 3.12 and
Jupyter. `test.ipynb` was inspected and re-executed successfully with PNG
output.

## What changed

### 1. User-wide Matplotlib defaults

Created:

`~/.matplotlib/matplotlibrc`

The default canvas is now `12.8 × 7.2` inches:

- `figure.dpi = 160`: approximately 2048 × 1152 for a 2K interactive canvas.
- `savefig.dpi = 300`: approximately 3840 × 2160 for a 4K saved raster before
  tight-boundary cropping.
- PNG is the default saved format.
- Tight bounding boxes, constrained layout, padding, antialiasing, clean
  typography, subtle grids, rounded lines, and publication-friendly spacing
  are enabled.
- PDF and PostScript use TrueType fonts (`fonttype = 42`).
- PNG is used for all default raster saves. PDF remains available when an
  explicitly requested vector document is needed.

These settings are neutral Matplotlib defaults, not a forced style sheet.
Calls such as the following continue to work normally:

```python
plt.style.use(matplotx.styles.ayu["light"])
```

The Ayu style was tested and changed the plot theme without changing the 2K/4K
quality settings.

### 2. High-density PNG output in Jupyter

Created:

`~/.ipython/profile_default/ipython_kernel_config.py`

The Jupyter inline backend now emits Retina PNG globally:

```python
%config InlineBackend.figure_format = "retina"
```

Retina mode produces a lossless `image/png` payload at twice the normal pixel
density and displays it at the intended logical size. With the global 160 DPI
canvas, the default inline raster is approximately 4096 × 2304 pixels before
tight-boundary cropping. Plot colors, fonts, and third-party styles are not
changed. New notebooks do not need a quality configuration cell.

### 3. Python 3.12 Jupyter kernel

Installed the default user kernel at:

`~/Library/Jupyter/kernels/python3/kernel.json`

The `python3` Jupyter kernel now uses:

`/opt/homebrew/opt/python@3.12/bin/python3.12`

Its display name is `Python 3.12`. Existing notebooks whose kernel name is
`python3`, including `test.ipynb`, resolve to this kernel.

## Normal usage

Standalone scripts need no quality boilerplate:

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.savefig("figure.png")
```

Jupyter notebooks also need no format or DPI setup cell. Third-party styles may
be used as usual.

Explicit arguments passed to `plt.figure`, `plt.subplots`, or `plt.savefig`
still take precedence. For example, an explicit `figsize=(8, 5)` or `dpi=300`
is respected.

## Validation performed

- Matplotlib 3.11.1 loaded `~/.matplotlib/matplotlibrc` under Python 3.12.14.
- A standalone PNG using the Matplotx Ayu light style rendered at 3876 × 2196
  after tight cropping.
- A clean Jupyter kernel reported the Python 3.12 executable and `retina` as its
  inline format.
- The Jupyter MIME bundle contained lossless `image/png` output and no SVG
  payload before any notebook-specific configuration was executed.
- Every code cell in `test.ipynb` executed successfully in a fresh kernel. Its
  embedded plot is a 2598 × 1638 RGBA PNG, and its saved `op_vs_n.png` is a
  2436 × 1536 RGBA PNG. Both have valid PNG signatures.

Restart an already-running Jupyter kernel once to pick up these permanent
settings. New Python processes and kernels use them automatically.
