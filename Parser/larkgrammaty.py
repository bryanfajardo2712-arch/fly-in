
GRAMMAR = r"""
start: ROL ":" NAME SIGNAL_INT SIGNAL_INT metadata?
metadata: "[" pair+ "]"
pair: KEY "=" VALUE
ROL: "start_hub" | "end_hub" | "hub"
NAME: /[^-\s\[\]]+/
SIGNAL_INT: /-?\d+/
KEY: /\w+/
VALUE: /[^\s\]]+/
%ignore " "
"""
