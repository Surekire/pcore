from evaluate import pcore_function, Context
from function_utiles import *




#args[0]: from
#args[1]: to
#args[2]: steps (optional)
@pcore_function("range")
def pcore_range(ctx: Context, args):
    args = eval_all_args(ctx, args)
    nums = [int(a) for a in args]

    if len(nums) not in (2, 3):
        raise ValueError("range erwartet 2 oder 3 Argumente: from, to[, steps]")

    return "[" + ",".join(str(n) for n in range(*nums)) + "]"

#args[0]: math input
@pcore_function("eval")
def pcore_eval(ctx: Context, args):
    arg = ctx.evaluate(args[0])
    return str(eval(arg))



#args[0]: join str
#args[1]: list of str to be joined, form [a,b,c]
@pcore_function("j")
def pcore_join(ctx: Context, args):
    sep = ctx.evaluate(args[0])
    items = read_str_list(ctx.evaluate(args[1]))
    return sep.join(items)

