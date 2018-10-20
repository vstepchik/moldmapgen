import random
from typing import List, Set

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

        self.infinite_regions = {i for i, r in enumerate(self.regions) if -1 in r}

        self.neighbor_points: List[Set[int]] = [set() for _ in range(len(self.points))]
        for a, b in self.ridge_points:
            self.neighbor_points[a].add(b)
            self.neighbor_points[b].add(a)

        self.neighbor_vertices: List[Set[int]] = [set() for _ in range(len(self.vertices))]
        for a, b in self.ridge_vertices:
            if a >= 0 and b >= 0:
                self.neighbor_vertices[a].add(b)
                self.neighbor_vertices[b].add(a)

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
        spread_p = np.random.uniform(0.3, 0.7, n)
        plates = [{p} for p in random.sample(range(len(self.points)), n)]
        taken = {p for point_set in plates for p in point_set}

        active_set = {n for region in plates for r in region for n in
                      list(self.neighbor_points[r])} - self.infinite_regions
        while active_set:
            to_remove: Set[int] = set()
            to_add: Set[int] = set()
            for region in active_set:
                if self.point_region[region] in self.infinite_regions:
                    to_remove.add(region)
                    continue

                neighbors = self.neighbor_points[region]
                candidates = neighbors & taken
                join_to = random.sample(candidates, 1)[0]
                pl, pi = next((p, i) for i, p in enumerate(plates) if join_to in p)
                if random.random() > spread_p[pi]:
                    continue

                pl.add(region)
                taken.add(region)
                to_remove.add(region)
                to_add |= (neighbors - taken - active_set)
            active_set = (active_set - to_remove) | to_add

        return plates
