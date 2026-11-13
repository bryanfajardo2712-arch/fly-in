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
    """Convierte el texto  de Max drones en un entero positvo"""
    try:
        num_drones = int(drones)
    except ValueError:
        raise ValueError(f"max_drones is not a number:'{drones}'")
    if num_drones <= 0:
        raise ValueError(f"Max_drones must to be a positive number '{drones}'")
    return num_drones


def assign_role(text: str) -> ZoneRol:
    return ZoneRol(text)


def assign_words(data: str) -> Zone:
    parts = data
    if "[" in parts:
        words = parts.split(" ", 4)
        role_text = (words[0].removesuffix(":"))
        name = (words[1])
        x = int(words[2])
        y = int(words[3])
        config = words[4].strip("[]")
        attributes = config.split()

        zone_type = ZoneType.NORMAL
        color = None
        for attribute in attributes:
            key, value = attribute.split("=")

            if key == "zone":
                zone_type = ZoneType(value)

            elif key == "color":
                color = value

            elif key == "max_drones":
                max_drones = read_max_drones(value)
    else:
        words = parts.split(" ", 3)
        role_text = (words[0].removesuffix(":"))
        name = (words[1])
        x = int(words[2])
        y = int(words[3])
        zone_type = ZoneType.NORMAL
        color = None

        role = assign_role(role_text)

    return Zone(
        name=name,
        x=x,
        y=y,
        zone_type=zone_type,
        color=color,
        role=role,
        max_drones=max_drones
    )


archivo = assign_words("hub: corridorA 4 3 [zone=priority color=green max_drones=2]")
print(archivo)
