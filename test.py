def pcore_function(arg=None):

    # Case 1: @pcore_function (no parentheses)
    if callable(arg):
        fn = arg
        print(fn.__name__)

    # Case 2: @pcore_function("name")
    def wrapper(fn):
        fn_name = arg or fn.__name__
        print(fn_name)

    return wrapper

@pcore_function
def f():
    print("Hallo ")

@pcore_function("w")
def g():
    print("Welt!")

