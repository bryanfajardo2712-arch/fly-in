import sys
from typing import cast
from lark import Lark
from lark.exceptions import UnexpectedInput, VisitError
from larkgrammaty import HUB_GRAMMAR, CONNECTION_GRAMMAR
from models import Zone
from transform_data import HubTransformer

parser = Lark(HUB_GRAMMAR, parser="lalr", transformer=HubTransformer())


def parse_file(path: str) -> list[Zone]:
    """Lee un archivo de mapa y devuelve sus zonas."""
    zones: list[Zone] = []
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
            zone = cast(Zone, parser.parse(line))
            zones.append(zone)
        except UnexpectedInput:
            print(f"Línea {number}: formato incorrecto")
            sys.exit(1)
        except VisitError as error:
            print(f"Línea {number}: {error.orig_exc}")
            sys.exit(1)
    return zones
