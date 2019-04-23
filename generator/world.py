from dataclasses import dataclass
from typing import Optional, List, Set, Tuple, TypeVar, Type, Dict

import numpy as np


@dataclass
class Space:
    width: int
    height: int


@dataclass
class Mesh:
    points: np.ndarray


@dataclass
class Plate:
    mesh_points: Set[int]
    velocity: Tuple[float, float] = (0.0, 0.0)
    color_rgb: Tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Tectonics:
    plates: List[Plate]


WorldPropType = TypeVar("WorldPropType")


class World:
    def __init__(self):
        self.props: Dict[Type[WorldPropType], WorldPropType] = {}

    def __getitem__(self, item: Type[WorldPropType]) -> Optional[WorldPropType]:
        return self.props.get(item, None)

    def __setitem__(self, key: Type[WorldPropType], value: Optional[WorldPropType]):
        self.props[key] = value
