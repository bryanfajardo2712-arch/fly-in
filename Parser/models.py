from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ZoneRol(Enum):
    START_HUB = "start_hub"
    HUB = "hub"
    END_HUB = "end_hub"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    role: ZoneRol = ZoneRol.HUB


@dataclass
class Connection:
    zone_a: Zone
    zone_b: Zone
    max_link_capacity: int = 1


def read_max_drones(drones: str) -> int:
    """Convierte el texto de max_drones en un entero positivo."""
    try:
        num_drones = int(drones)
    except ValueError:
        raise ValueError(f"'max_drones' is not a number: '{drones}'")
    if num_drones <= 0:
        raise ValueError(f"'max_drones' must be a positive number: '{drones}'")
    return num_drones
