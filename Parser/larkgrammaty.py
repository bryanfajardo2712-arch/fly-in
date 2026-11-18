
HUB_GRAMMAR = r"""
start: ROL ":" NAME SIGNAL_INT SIGNAL_INT metadata?
metadata: "[" pair+ "]"
pair: KEY "=" VALUE
ROL: "start_hub" | "end_hub" | "hub"
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
SIGNAL_INT: /-?\d+/
KEY: /\w+/
VALUE: /[^\s\]]+/
%ignore " "

%import common.WS
%ignore WS
"""

CONNECTION_GRAMMAR = r"""
start: ROL ":" zone metada?
zone: NAME "-" NAME
metadata: "[" "max_link_capacity" "=" VALUE"]"
ROL: "connection"
NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
VALUE: /\d+/
%ignore " "

%import common.WS
%import WS

"""
