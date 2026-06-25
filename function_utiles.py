from evaluate import pcore_function, Context
def eval_all_args(ctx : Context, args):
    return [ ctx.evaluate(a) for a in args ]

def read_str_list(str : str):
    return list(str.strip("[]").split(","))