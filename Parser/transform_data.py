from typing import Any
from lark import Token, Transformer
from models import Zone, ZoneRol, ZoneType, read_max_drones
from models import Connection


class HubTransformer(Transformer[Token, Zone]):
    def pair(self, items: list[Token]) -> tuple[str, str]:
        return (str(items[0]), str(items[1]))

    def metadata(self, items: list[tuple[str, str]]) -> dict[str, str]:
        return dict(items)

    def start(self, items: list[Any]) -> Zone:
        role = ZoneRol(str(items[0]))
        name = str(items[1])
        x = int(items[2])
        y = int(items[3])
        meta: dict[str, str] = items[4] if len(items) > 4 else {}

        zone_type = ZoneType.NORMAL
        color: str | None = None
        max_drones = 1

        for key, value in meta.items():
            if key == "zone":
                zone_type = ZoneType(value)
            elif key == "color":
                color = value
            elif key == "max_drones":
                max_drones = read_max_drones(value)
            else:
                raise ValueError(f"Unknown attribute: '{key}'")

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=color,
            role=role,
            max_drones=max_drones,
        )


class ConnectionTransformer(Transformer[Token, Connection]):
    def __init__(self, zones_by_name: dict[str, Zone]) -> None:
        super().__init__()
        self.zones_by_name = zones_by_name

    def zone(self, items: list[Token]) -> tuple[str, str]:
        return (str(items[0]), str(items[1]))

    def metadata(self, items: list[Token]) -> int:
        capacity = int(items[0])
        if capacity <= 0:
            raise ValueError(f"'max_link_capacity' must be"
                             f" positve: '{capacity}'")
        return capacity

    def start(self, items: list[Any]) -> Connection:
        name_a, name_b = items[1]
        max_link_capacity: int = items[2] if len(items) > 2 else 1

        if name_a not in self.zones_by_name:
            raise ValueError(f"Zona desconocida en conexion: '{name_a}'")
        if name_b not in self.zones_by_name:
            raise ValueError(f"zona desconocida en conexion: '{name_b}'")

        return Connection(
            zone_a=self.zones_by_name[name_a],
            zone_b=self.zones_by_name[name_b],
            max_link_capacity=max_link_capacity
        )


class NbDronesTransformer(Transformer[Token, int]):
    def start(self, items: list[Token]) -> int:
        nb_drones = int(items[-1])
        if nb_drones <= 0:
            raise ValueError(f"'nb_drones' must be a "
                             f"positive number: '{nb_drones}'")
        return nb_drones
