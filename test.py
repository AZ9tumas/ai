import matplotlib.pyplot as plt
import matplotx
import numpy as np
# plt.style.use(matplotx.styles.ayu['light'])
# plt.style.use(matplotx.styles.ayu['light'])


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
plt.plot(n_values, op_values, marker='o',
         linestyle='-', linewidth=2, label="op(n)")
plt.plot(n_values, n_values, marker='o',
         linestyle='-', linewidth=2, label="linear")
plt.plot(n_values, n_values ** 2, marker='o',
         linestyle='-', linewidth=2, label="quadratic")
plt.plot(n_values, np.log(n_values), marker='o',
         linestyle='-', linewidth=2, label="log")
plt.title('Operations (op) vs Array Size (n)')
plt.xlabel('n')
plt.ylabel('op')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(n_values)
plt.legend()
# plt.tight_layout()
plt.show()
