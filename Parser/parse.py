import sys
from typing import cast
from lark import Lark
from lark.exceptions import UnexpectedInput, VisitError
from larkgrammaty import HUB_GRAMMAR, CONNECTION_GRAMMAR, NB_GRAMMAR
from models import Zone, Connection
from transform_data import (
    HubTransformer,
    ConnectionTransformer,
    NbDronesTransformer)


def parse_file(path: str) -> tuple[list[Zone], list[Connection]]:
    """Lee un archivo de mapa y devuelve sus zonas."""
    nb_drones: int | None = None
    zones_by_name: dict[str, Zone] = {}
    connections: list[Connection] = []

    nb_parser = Lark(NB_GRAMMAR, parser="lalr",
                     transformer=NbDronesTransformer())
    hub_parser = Lark(HUB_GRAMMAR, parser="lalr", transformer=HubTransformer())
    conn_parser = Lark(
        CONNECTION_GRAMMAR,
        parser="lalr",
        transformer=ConnectionTransformer(zones_by_name)
    )
    try:
        with open(path) as file:
            lines = file.readlines()
    except OSError as error:
        print(f"Error: no se puede leer '{path}': {error}")
        sys.exit(1)

    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        try:
            if line.startswith("nb_drones:"):
                if nb_drones is not None:
                    raise ValueError("nb_drones' está definido más de una vez")
                nb_drones = cast(int, nb_parser.parse(line))
            elif line.startswith("connection:"):
                connection = cast(Connection, conn_parser.parse(line))
                connections.append(connection)
            else:
                zone = cast(Zone, hub_parser.parse(line))
                if zone.name in zones_by_name:
                    raise ValueError(f"Zona duplicada: '{zone.name}'")
                zones_by_name[zone.name] = zone

        except UnexpectedInput as e:
            print(f"Línea {number}: formato incorrecto")
            print(e)
            sys.exit(1)
        except VisitError as error:
            print(f"Línea {number}: {error.orig_exc}")
            sys.exit(1)
        except ValueError as error:
            print(f"Línea {number}: {error}")
            sys.exit(1)

    return list(zones_by_name.values()), connections


if __name__ == "__main__":
    zones, connections = parse_file("mapa1.txt")
    print(zones)
    print(connections)
