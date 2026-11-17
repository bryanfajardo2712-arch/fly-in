from lark import Lark
from lark.exceptions import UnexpectedInput
from larkgrammaty import GRAMMAR
from dataclasses import dataclass
from enum import Enum

parser = Lark(GRAMMAR)


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
    """Convierte el texto  de Max drones en un entero positvo"""
    try:
        num_drones = int(drones)
    except ValueError:
        raise ValueError(f"'max_drones' is not a number:'{drones}'")
    if num_drones <= 0:
        raise ValueError(f"'max_drones' must to"
                         f"be a positive number:'{drones}'")
    return num_drones


def assign_role(text: str) -> ZoneRol:
    return ZoneRol(text)


def assign_words(data: str) -> Zone:
    head, _, meta = data.partition("[")
    words = head.split()
    role = assign_role(words[0].removesuffix(":"))
    name = words[1]
    x = int(words[2])
    y = int(words[3])
    zone_type = ZoneType.NORMAL
    color = None
    max_drones = 1
    for attribute in meta.strip("] \n").split():
        key, value = attribute.split("=")
        if key == "zone":
            zone_type = ZoneType(value)
        elif key == "color":
            color = value
        elif key == "max_drones":
            max_drones = read_max_drones(value)

    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=zone_type,
        color=color,
        role=role,
        max_drones=max_drones
    )


try:
    tree = parser.parse("4ub: roof1 3 4 [zone=restricted]")
except UnexpectedInput as e:
    print(f"format error on the line : {e.line}, column {e.column}")
