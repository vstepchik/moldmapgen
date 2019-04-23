import abc
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Optional, List, Set, Tuple, TypeVar, Type

import numpy as np


class WorldProp(abc.ABC):
    pass


@dataclass
class Space(WorldProp):
    width: int
    height: int


@dataclass
class Mesh(WorldProp):
    points: np.ndarray


@dataclass
class Plate:
    mesh_points: Set[int] = field(default_factory=set)
    velocity: Tuple[float, float] = (0.0, 0.0)
    spin_rad: float = 0.0
    color_rgb: Tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class Tectonics(WorldProp):
    plates: List[Plate]


WorldPropType = TypeVar("WorldPropType")


class World:
    def __init__(self):
        self.props: OrderedDict[Type[WorldPropType], WorldPropType] = OrderedDict()

    def __getitem__(self, item: Type[WorldPropType]) -> Optional[WorldPropType]:
        return self.props.get(item, None)

    def __setitem__(self, key: Type[WorldPropType], value: Optional[WorldPropType]):
        self.props[key] = value
