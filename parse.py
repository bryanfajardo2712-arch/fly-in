from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ZoneRol(Enum):
    START = "start"
    REGULAR = "regular"
    END = "end"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    role: ZoneRol = ZoneRol.REGULAR


@dataclass
class Connection:
    zone_a: Zone
    zone_b: Zone
    max_link_capacity: int = 1


def assign_words(data: str) -> Zone:
    parts = data.split(" ", 4)
    name = (parts[1])
    x = int(parts[2])
    y = int(parts[3])
    config = parts[4].strip("[]")
    attributes = config.split()

    zone_type = ZoneType.NORMAL
    color = None
    for attribute in attributes:
        key, value = attribute.split("=")

        if key == "zone":
            zone_type = ZoneType(value)

        elif key == "color":
            color = value

    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=zone_type,
        color=color
    )