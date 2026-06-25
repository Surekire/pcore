from parser import NodeRef, Text, FunctionCall, Concat, VariableRef, Parser

FUNCTIONS = {}

def pcore_function(arg=None):

    # Case 1: @pcore_function (no parentheses)
    if callable(arg):
        fn = arg
        FUNCTIONS[fn.__name__] = fn
        return fn

    # Case 2: @pcore_function("name")
    def wrapper(fn):
        fn_name = arg or fn.__name__
        FUNCTIONS[fn_name] = fn
        return fn

    return wrapper

class Context:
    def __init__(self, functions=None):
        self.nodes = {}
        self.cache = {}
        self.variables = {}

        self.functions = functions or FUNCTIONS

    def register_node(self, name, str):
        self.nodes[name] = Parser(str).parse_expression()

    def get_node_output(self, node_id):

        if node_id in self.cache:
            return self.cache[node_id]

        ast = self.nodes[node_id]

        result = self.evaluate(ast)

        self.cache[node_id] = result

        return result

    def evaluate(self, node):

        if isinstance(node, NodeRef):
            return self.get_node_output(node.id)
        
        if isinstance(node, Text):
            return node.value
        
        if isinstance(node, FunctionCall):
            fn = self.functions[node.name]
            return fn(self, node.args)
        
        if isinstance(node, Concat):
            return "".join(self.evaluate(p) for p in node.parts)
        
        if isinstance(node, VariableRef):
            return self.variables[node.name]
