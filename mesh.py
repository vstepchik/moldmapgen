from typing import List

import noise
import numpy as np
from numpy.core.multiarray import ndarray
from scipy.spatial.qhull import Voronoi


class Mesh:
    def __init__(self, vor: Voronoi):
        self.points: ndarray = vor.points
        self.vertices: ndarray = vor.vertices
        self.ridge_points: ndarray = vor.ridge_points
        self.ridge_vertices: List[List[int]] = vor.ridge_vertices
        self.regions: List[List[int]] = vor.regions
        self.point_region: List[int] = vor.point_region

        self.noise: ndarray = None

    def create_noise(self):
        self.noise = np.zeros(len(self.vertices), 'float32')
        scale = 128  # fixme: should depend on map size
        for i in range(len(self.vertices)):
            coordinates = self.vertices[i]
            lvl = noise.snoise2(
                coordinates[0] / scale,
                coordinates[1] / scale,
                octaves=4,
                persistence=0.5,
                lacunarity=1.9,
                base=0,
            )
            self.noise[i] = (lvl + 1) / 2.0

    def create_tectonic_plates(self, n: int):
        regions = np.random.choice(self.point_region, n, replace=False)
        print(regions)
        return regions
