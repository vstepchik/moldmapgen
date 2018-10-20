import random
from typing import Set, List

import numpy as np

from mesh import Mesh


class Geo:
    def __init__(self, mesh: Mesh) -> None:
        self.mesh = mesh

    def create_tectonic_plates(self, n: int) -> List[Set[int]]:
        starting_regions = random.sample(range(len(self.mesh.points)), n)
        plates = [{p} for p in starting_regions]
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

        return plates
