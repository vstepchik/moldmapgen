import random
from colorsys import hsv_to_rgb
from typing import Set, List, Tuple

import numpy as np

from mesh import Mesh


class Plate(Set[int]):
    velocity: Tuple[float, float] = (0.0, 0.0)
    color: Tuple[float, float, float] = (0.0, 0.0, 0.0)


class Geo:
    def __init__(self, mesh: Mesh) -> None:
        self.mesh = mesh

    def create_tectonic_plates(self, n: int) -> List[Plate]:
        starting_regions = random.sample(range(len(self.mesh.points)), n)
        plates = [Plate([p]) for p in starting_regions]
        taken = {p for point_set in plates for p in point_set}
        spread_probabilities = np.random.uniform(0.3, 0.7, n)

        active_set = {n for r in starting_regions for n in list(self.mesh.neighbor_points[r])}
        active_set -= self.mesh.infinite_regions
        while active_set:
            to_remove: Set[int] = set()
            to_add: Set[int] = set()
            for region in active_set:
                if self.mesh.point_region[region] in self.mesh.infinite_regions:
                    to_remove.add(region)
                    continue

                neighbors = self.mesh.neighbor_points[region]
                candidates = neighbors & taken
                join_to = random.sample(candidates, 1)[0]
                pl, pi = next((p, i) for i, p in enumerate(plates) if join_to in p)

                if random.random() > spread_probabilities[pi]:
                    continue

                pl.add(region)
                taken.add(region)
                to_remove.add(region)
                to_add |= (neighbors - taken - active_set)
            active_set = (active_set - to_remove) | to_add

        for i, plate in enumerate(plates):
            plate.velocity = tuple(np.random.uniform(-1.0, 1.0, 2))
            plate.color = hsv_to_rgb(float(i) / len(plates), 0.9, 0.7)

        return plates
