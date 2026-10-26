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