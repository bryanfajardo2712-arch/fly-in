from typing import Any
from lark import Token, Transformer
from models import Zone, ZoneRol, ZoneType, read_max_drones


class HubTransformer(Transformer[Token, Zone]):
    def pair(self, items: list[Token]) -> tuple[str, str]:
        return (str(items), str(items))

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


class ConnectionTransformer(Transformer[Token, Zone, Zone]):
    def metadata(self, items: list[tuple[str, str]]) -> dict[str, str]:
        return dict(items)

    def zone(self, items: list[Token]) -> tuple[str, str]:
        return (str(items), str(items))

    def start(self, items: list[Any]) -> Connection:
        zone_a = items[1]
        zone_b = items[2]
        max_link_capacity = 1
        if len[items] > 3:
            max_link_capacity = items[4]

        return Connection(
            zone_a= zone_a,
            zone_b= zone_b,
            max_link_capacity= max_link_capacity
        )