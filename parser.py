from dataclasses import dataclass

@dataclass
class Text:
    value: str

@dataclass
class NodeRef:
    id: str

@dataclass
class FunctionCall:
    name: str
    args: list

@dataclass
class Concat:
    parts: list

@dataclass
class VariableRef:
    name: str

class Parser:
    def __init__(self, text):
        self.text = text
        self.i = 0
        self.n = len(text)

    def peek(self):
        return self.text[self.i] if self.i < self.n else None

    def next(self):
        ch = self.peek()

        if ch == "\\":
            self.i += 1
            esc = self.peek()

            if esc is None:
                return "\\"

            self.i += 1

            return self.translate_escape(esc)

        self.i += 1
        return ch
    
    def translate_escape(self,c):
        return {
            "n": "\n",
            "t": "\t",
            "\\": "\\",
            "$": "$",
            "(": "(",
            ")": ")",
            ",": ",",
            " ": "",
        }.get(c, c)

    def parse_expression(self, stop_chars=None):
        stop_chars = stop_chars or set()

        parts = []

        while self.i < self.n:

            if self.peek() in stop_chars:
                break

            old_i = self.i
            ch = self.peek()

            if ch == "$":
                parts.append(self.parse_node_ref())

            elif ch.isalpha() or ch == " " or ch == "_":
                tmp_part = self.parse_maybe_function_or_text()
                if isinstance(tmp_part, Text) and len(parts) != 0 and isinstance(parts[-1], Text):
                    parts[-1].value += tmp_part.value
                else:
                    parts.append(tmp_part)

            elif ch == "@":
                parts.append(self.parse_variable_ref())

            else:
                parts.append(self.parse_text(stop_chars))

            if self.i == old_i:
                raise RuntimeError(
                    f"Parser made no progress at position {self.i}: {repr(self.peek())}"
                )

        if len(parts) == 1:
            return parts[0]

        return Concat(parts)

    def parse_node_ref(self):
        self.next()  # consume $

        start = self.i
        while self.peek() != "$":
            self.next()

        node_id = self.text[start:self.i]
        self.next()  # closing $

        return NodeRef(node_id)

    def parse_maybe_function_or_text(self):
        start = self.i

        # read name
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            self.next()

        if self.peek() == " ":
            self.next()


        name = self.text[start:self.i]

        if self.peek() == "(":
            if name == " ":
                raise SyntaxError(f"SyntaxError at pos: {self.i} Funktion Name Cannot be \" \"")
            return self.parse_function_call(name)

        return Text(name)


    def skip_whitespace(self):
        while self.peek() is not None and self.peek().isspace():
            self.next()

    def parse_function_call(self, name):
        self.next()  # consume '('

        args = []

        while True:

            self.skip_whitespace()

            if self.peek() == ")":
                self.next()
                break

            args.append(
                self.parse_expression(
                    stop_chars={",", ")"}
                )
            )

            self.skip_whitespace()

            if self.peek() == ",":
                self.next()
                continue

            if self.peek() == ")":
                self.next()
                break

            raise SyntaxError(
                f"Expected ',' or ')' at position {self.i}"
            )

        return FunctionCall(name, args)


    def parse_text(self, stop_chars=None):
        stop_chars = stop_chars or set()

        result = []

        while True:
            ch = self.peek()

            # Ende der Expression / Block
            if ch is None:
                break

            if ch in stop_chars:
                break

            # PCore-Syntax Grenzen
            if ch == "$":
                break

            if ch == "(":
                break

            if ch == "@":
                break

            # normales Zeichen konsumieren (inkl. bereits ge-escaped chars)
            result.append(self.next())

        return Text("".join(result))
    
    def parse_variable_ref(self, stop_chars=None):
        self.next()
        
        stop_chars = stop_chars or set([" "])
        result = []


        while True:
            ch = self.peek()

            # Ende der Expression / Block
            if ch is None:
                break

            if ch.isalnum() or ch == "_":
                result.append(self.next())
                
            else:
                break

        return VariableRef("".join(result))

    
def dump(node, indent=0):
    pad = "  " * indent

    if isinstance(node, Text):
        print(f"{pad}Text({node.value!r});")

    elif isinstance(node, NodeRef):
        print(f"{pad}NodeRef({node.id});")

    elif isinstance(node, FunctionCall):
        print(f"{pad}Function({node.name}):")
        for arg in node.args:
            dump(arg, indent + 1)

    elif isinstance(node, Concat):
        print(f"{pad}Concat:")
        for part in node.parts:
            dump(part, indent + 1)

    elif isinstance(node, VariableRef):
        print(f"{pad}VariableRef({node.name})")

