HUB_GRAMMAR = r"""
start: ROL ":" NAME SIGNAL_INT SIGNAL_INT metadata?
metadata: "[" pair+ "]"
pair: KEY "=" VALUE
ROL: "start_hub" | "end_hub" | "hub"
NAME: /[^-\s\[\]]+/
SIGNAL_INT: /-?\d+/
KEY: /\w+/
VALUE: /[^\s\]]+/
%ignore /[ \t]+/
"""

CONNECTION_GRAMMAR = r"""
start: CONNECTION ":" zone metadata?
zone: NAME "-" NAME
metadata: "[" "max_link_capacity" "=" VALUE"]"
CONNECTION: "connection"
NAME: /[^-\s\[\]]+/
VALUE: /\d+/
%ignore /[ \t]+/
"""

NB_GRAMMAR = r"""
start: NDRONES ":" INT
INT: /\d+/
NDRONES: "nb_drones"
%ignore /[ \t]+/
"""
