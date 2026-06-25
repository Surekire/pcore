from evaluate import pcore_function, Context
from function_utiles import *


@pcore_function("l")
def tolist(ctx : Context, args):
    args = [ ctx.evaluate(a) for a in args ]
    return "[" + ",".join(args) + "]"

#args[0] to reapeatet Text
#args[1] number of repeats
@pcore_function("r")
def repeat(ctx : Context, args):
    args = [ ctx.evaluate(a) for a in args ]
    a = int(args[1])
    return args[0]*a

#args[0] term with replace varaibles @a @b @c
#args[1] variable names as list of form [a,b,c,...]
#args[2..] list lists
@pcore_function("for")
def for_list(ctx: Context, args):

    template = args[0]
    var_name_list = read_str_list(ctx.evaluate(args[1]))
    lists = args[2:]

    if len(var_name_list) < len(lists):
        raise ValueError(
            "Not enough variable names for provided lists"
        )

    evaluated_lists = [read_str_list(ctx.evaluate(l)) for l in lists]

    result = []

    for row in zip(*evaluated_lists):

        old_values = {}

        for value, var_name in zip(row, var_name_list):
            old_values[var_name] = ctx.variables.get(var_name)
            ctx.variables[var_name] = value

        result.append(ctx.evaluate(template))

        for var_name in var_name_list:
            if old_values[var_name] is None:
                ctx.variables.pop(var_name, None)
            else:
                ctx.variables[var_name] = old_values[var_name]

    return "".join(result)


#args[0] var
#args[1] value
@pcore_function("sv")
def setvar(ctx : Context, args):
    args = [ ctx.evaluate(a) for a in args ]
    ctx.variables[args[0]] = args[1]
    return ""
