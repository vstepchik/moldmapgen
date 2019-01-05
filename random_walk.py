import cv2
import numpy as np

N = 5_000_000
PROGRESS_STEP = 5

print("Generating movements...")
points = np.random.randint(-1, 2, N * 2, 'int8').reshape(N, 2)

actor = (0, 0)
dims = (0, 0, 0, 0)
path = []

print("Calculating path...")
stops = len(points) // 100 * PROGRESS_STEP
for i, p in enumerate(points):
    path.append(tuple(actor))
    actor += p
    dims = (min(dims[0], actor[0]), min(dims[1], actor[1]), max(dims[2], actor[0]), max(dims[3], actor[1]))
    if i % stops == stops - 1:
        print((i + 1) // stops * PROGRESS_STEP, '%')
del stops
del points
del actor

print('dims =', dims)
w, h = abs(dims[0] - dims[2]), abs(dims[1] - dims[3])

print('w =', w, 'h =', h)
mat = np.zeros((w, h), 'uint16')
offset = (-dims[0] - 1, -dims[1] - 1)
max_val = 0

print("Drawing path...")
stops = len(path) // 100 * PROGRESS_STEP
for i, p in enumerate(path):
    x = p[0] + offset[0]
    y = p[1] + offset[1]
    mat[x, y] += 1
    max_val = max(max_val, mat[x, y])
    if i % stops == stops - 1:
        print((i + 1) // stops * PROGRESS_STEP, '%')

print('max_val =', max_val)
print("Multiplying brightness...")
mat *= (65535 // max_val)

fname = 'out.png'
cv2.imwrite(fname, mat)
print('Done! Check out the', fname)
