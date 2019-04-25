from typing import List, Set, Optional

import numpy as np

from atlas import Atlas
from generator.ctrl.steps.mesh.config import MeshConfig
from generator.ctrl.steps.step import GeneratorStep
from generator.world import World, Mesh, Space


class MeshCreationStep(GeneratorStep[MeshConfig]):
    def run(self, world: World) -> Optional[Mesh]:
        space: Space = world[Space]
        if space is None:
            return None

        node_amount = int(self.config.node_density * space.area)
        atlas = Atlas(dimensions=(space.width, space.height), granularity=node_amount)
        atlas.generate_voronoi()

        points: np.ndarray = atlas.vor.points
        vertices: np.ndarray = atlas.vor.vertices
        ridge_points: np.ndarray = atlas.vor.ridge_points
        ridge_vertices: List[List[int]] = atlas.vor.ridge_vertices
        regions: List[List[int]] = atlas.vor.regions
        point_region: List[int] = atlas.vor.point_region

        infinite_regions = {i for i, r in enumerate(regions) if -1 in r}

        neighbor_points: List[Set[int]] = [set() for _ in range(len(points))]
        for a, b in ridge_points:
            neighbor_points[a].add(b)
            neighbor_points[b].add(a)

        neighbor_vertices: List[Set[int]] = [set() for _ in range(len(vertices))]
        for a, b in ridge_vertices:
            if a >= 0 and b >= 0:
                neighbor_vertices[a].add(b)
                neighbor_vertices[b].add(a)

        return Mesh(
            points=points,
            vertices=vertices,
            ridge_points=ridge_points,
            ridge_vertices=ridge_vertices,
            regions=regions,
            point_region=point_region,
            infinite_regions=infinite_regions,
            neighbor_points=neighbor_points,
            neighbor_vertices=neighbor_vertices,
        )
