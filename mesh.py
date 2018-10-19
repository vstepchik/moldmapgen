from typing import List

import noise
import numpy as np
from numpy.core.multiarray import ndarray

from atlas import Atlas


class Mesh:
    def __init__(self, dimensions: (int, int), npoints: int, relax_steps: int = 0):
        vor = Atlas(dimensions=dimensions, granularity=npoints)
        vor.generate_voronoi()
        vor = vor.relax_points(relax_steps)

        self.points: ndarray = vor.points
        self.vertices: ndarray = vor.vertices
        self.ridge_points: ndarray = vor.ridge_points
        self.ridge_vertices: List[List[int]] = vor.ridge_vertices
        self.regions: List[List[int]] = vor.regions
        self.point_region: List[int] = vor.point_region

        self.neighbor_points: List[List[int]] = [[] for _ in range(len(self.points))]
        for i, j in self.ridge_points:
            self.neighbor_points[i].append(j)
            self.neighbor_points[j].append(i)

        self.neighbor_vertices: List[List[int]] = [[] for _ in range(len(self.vertices))]
        for i, j in self.ridge_vertices:
            self.neighbor_vertices[i].append(j)
            self.neighbor_vertices[j].append(i)

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
