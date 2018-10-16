import cv2
import numpy as np
from scipy.spatial import Voronoi

_MAP_SIZE = 2048
_DOTS_DENSITY = 0.004

_DOTS_AMOUNT = int(_MAP_SIZE * _MAP_SIZE * _DOTS_DENSITY)


class T:
    from datetime import datetime
    dt = datetime

    def __init__(self):
        self.__t = T.dt.utcnow()

    def p(self, label: str):
        now = T.dt.utcnow()
        print(now - self.__t, label)
        self.__t = now


t = T()
img = np.zeros((_MAP_SIZE, _MAP_SIZE, 3), np.uint8)
points = np.random.rand(2, _DOTS_AMOUNT) * _MAP_SIZE
t.p(f"{_DOTS_AMOUNT} points generated")

vor = Voronoi(points.reshape([_DOTS_AMOUNT, 2]))
t.p("voronoi build")

for i in range(len(vor.ridge_vertices)):
    if vor.ridge_vertices[i][0] < 0:
        continue
    coordinates = vor.vertices[vor.ridge_vertices[i]]
    cv2.line(img, tuple(coordinates[0].astype(int)), tuple(coordinates[1].astype(int)), (153, 0, 0), 1)

for i in range(len(vor.ridge_points)):
    if vor.ridge_points[i][0] < 0:
        continue
    coordinates = vor.points[vor.ridge_points[i]]
    cv2.line(img, tuple(coordinates[0].astype(int)), tuple(coordinates[1].astype(int)), (0, 0, 102), 1)

t.p("voronoi drawn")

if 0:
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 20
    fig_size[1] = 20
    voronoi_plot_2d(vor)
    plt.show()

if 1:
    cv2.imshow("output", img)
    cv2.waitKey()
