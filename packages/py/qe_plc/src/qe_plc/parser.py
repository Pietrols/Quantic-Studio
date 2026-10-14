"""Recursive-descent parser and static type checker for the Structured Text subset.

Grammar and semantics: docs/specs/structured-text-subset.md. Operator precedence
follows Bolton, Programmable Logic Controllers, 6th ed (Newnes, 2015), Table 6.3,
p. 168, from lowest to highest: OR; XOR; AND and &; = and <>; <, >, <= and >=;
+ and -; *, / and MOD; unary - and NOT; **; parentheses.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .errors import PlcError
from .lexer import Token, tokenize

ELEMENTARY = {"BOOL", "INT", "REAL", "TIME"}
# Function-block interfaces: (inputs, outputs) with their types.
BLOCKS = {
    "TON": ({"IN": "BOOL", "PT": "TIME"}, {"Q": "BOOL", "ET": "TIME"}),
    "TOF": ({"IN": "BOOL", "PT": "TIME"}, {"Q": "BOOL", "ET": "TIME"}),
    "TP": ({"IN": "BOOL", "PT": "TIME"}, {"Q": "BOOL", "ET": "TIME"}),
    "CTU": ({"CU": "BOOL", "R": "BOOL", "PV": "INT"}, {"Q": "BOOL", "CV": "INT"}),
    "CTD": ({"CD": "BOOL", "LD": "BOOL", "PV": "INT"}, {"Q": "BOOL", "CV": "INT"}),
    "CTUD": ({"CU": "BOOL", "CD": "BOOL", "R": "BOOL", "LD": "BOOL", "PV": "INT"},
             {"QU": "BOOL", "QD": "BOOL", "CV": "INT"}),
}
SECTIONS = {"VAR_INPUT": "input", "VAR_OUTPUT": "output", "VAR": "var"}


@dataclass
class Expr:
    line: int
    column: int
    type: str = ""


@dataclass
class Literal(Expr):
    value: object = None


@dataclass
class Name(Expr):
    key: str = ""


@dataclass
class Member(Expr):
    instance: str = ""
    field: str = ""


@dataclass
class Unary(Expr):
    op: str = ""
    operand: Expr | None = None


@dataclass
class Binary(Expr):
    op: str = ""
    left: Expr | None = None
    right: Expr | None = None


@dataclass
class Decl:
    name: str
    key: str
    section: str
    type: str
    initial: object
    line: int
    column: int


@dataclass
class Assign:
    target: str
    expr: Expr
    text: str
    line: int
    column: int


@dataclass
class If:
    branches: list  # [(condition Expr, condition text, [statements])]
    otherwise: list | None
    line: int
    column: int


@dataclass
class Call:
    instance: str
    params: list  # [(input name, Expr, text)]
    line: int
    column: int


@dataclass
class Program:
    name: str
    decls: dict = field(default_factory=dict)  # key -> Decl, in declaration order
    body: list = field(default_factory=list)


def _default(type_name):
    return {"BOOL": False, "INT": 0, "REAL": 0.0, "TIME": 0}[type_name]


class _Parser:
    def __init__(self, source: str):
        self.source = source
        self.lines = source.splitlines()
        self.tokens = tokenize(source)
        self.i = 0

    # token helpers
    def peek(self, offset=0) -> Token:
        return self.tokens[min(self.i + offset, len(self.tokens) - 1)]

    def take(self) -> Token:
        token = self.peek()
        self.i += 1
        return token

    def accept(self, text) -> Token | None:
        token = self.peek()
        if token.kind in ("OP", "KEYWORD") and token.text == text:
            return self.take()
        return None

    def expect(self, text) -> Token:
        token = self.peek()
        if token.kind in ("OP", "KEYWORD") and token.text == text:
            return self.take()
        found = token.text or "end of program"
        raise PlcError("SYNTAX", f"Expected {text} but found {found}", token.line, token.column)

    def name(self) -> Token:
        token = self.peek()
        if token.kind != "NAME":
            raise PlcError("SYNTAX", f"Expected a name but found {token.text or 'end of program'}",
                           token.line, token.column)
        return self.take()

    def span(self, start: Token, end: Token) -> str:
        """Source text from token start up to (not including) token end, for traces."""
        if start.line == end.line:
            return self.lines[start.line - 1][start.column - 1:end.column - 1].strip()
        first = self.lines[start.line - 1][start.column - 1:]
        middle = self.lines[start.line:end.line - 1]
        last = self.lines[end.line - 1][:end.column - 1]
        return " ".join(part.strip() for part in (first, *middle, last) if part.strip())

    # program
    def program(self) -> Program:
        self.expect("PROGRAM")
        program = Program(self.name().text)
        while self.peek().text in SECTIONS:
            section = SECTIONS[self.take().text]
            while not self.accept("END_VAR"):
                self.declaration(program, section)
        program.body = self.statements({"END_PROGRAM"})
        self.expect("END_PROGRAM")
        if self.peek().kind != "EOF":
            token = self.peek()
            raise PlcError("SYNTAX", "Text after END_PROGRAM", token.line, token.column)
        return program

    def declaration(self, program, section):
        names = [self.name()]
        while self.accept(","):
            names.append(self.name())
        self.expect(":")
        type_token = self.take()
        type_name = type_token.text if type_token.kind == "KEYWORD" else ""
        if type_name not in ELEMENTARY and type_name not in BLOCKS:
            raise PlcError("UNKNOWN_TYPE", f"Unknown or unsupported type {type_token.text}",
                           type_token.line, type_token.column)
        if type_name in BLOCKS and section != "var":
            raise PlcError("UNSUPPORTED_SYNTAX", "Function-block instances belong in VAR",
                           type_token.line, type_token.column)
        initial = None
        if self.accept(":="):
            if type_name in BLOCKS:
                token = self.peek()
                raise PlcError("UNSUPPORTED_SYNTAX", "Function-block instances take no initial value",
                               token.line, token.column)
            initial = self.constant(type_name)
        self.expect(";")
        for token in names:
            key = token.text.upper()
            if key in program.decls:
                raise PlcError("DUPLICATE_NAME", f"{token.text} is declared twice", token.line, token.column)
            if section == "input" and initial is not None:
                raise PlcError("UNSUPPORTED_SYNTAX", "Inputs take their value from the input image",
                               token.line, token.column)
            value = initial if initial is not None else (None if type_name in BLOCKS else _default(type_name))
            program.decls[key] = Decl(token.text, key, section, type_name, value, token.line, token.column)

    def constant(self, type_name):
        token = self.peek()
        negative = bool(self.accept("-"))
        token = self.take()
        kinds = {"BOOL": ("KEYWORD",), "INT": ("INT",), "REAL": ("REAL", "INT"), "TIME": ("TIME",)}
        if token.kind not in kinds[type_name] or (type_name == "BOOL" and token.text not in ("TRUE", "FALSE")):
            raise PlcError("TYPE_MISMATCH", f"Initial value {token.text} does not fit {type_name}",
                           token.line, token.column)
        value = (token.text == "TRUE") if type_name == "BOOL" else token.value
        if type_name == "REAL":
            value = float(value)
        if negative:
            if type_name == "BOOL":
                raise PlcError("TYPE_MISMATCH", "A BOOL cannot be negated with -", token.line, token.column)
            value = -value
        if type_name == "INT" and not -32768 <= value <= 32767:
            raise PlcError("INT_OVERFLOW", f"{value} is outside INT (-32768 to 32767)", token.line, token.column)
        return value

    # statements
    def statements(self, stops) -> list:
        body = []
        while self.peek().text not in stops or self.peek().kind not in ("KEYWORD",):
            token = self.peek()
            if token.kind == "EOF":
                raise PlcError("SYNTAX", "Program ended before " + " or ".join(sorted(stops)),
                               token.line, token.column)
            if self.accept(";"):
                continue
            if token.kind == "KEYWORD" and token.text == "IF":
                body.append(self.if_statement())
            elif token.kind == "NAME" and self.peek(1).text == ":=":
                body.append(self.assignment())
            elif token.kind == "NAME" and self.peek(1).text == "(":
                body.append(self.call())
            else:
                raise PlcError("SYNTAX", f"Unexpected {token.text}: expected an assignment, IF or block call",
                               token.line, token.column)
        return body

    def assignment(self):
        target = self.take()
        self.expect(":=")
        start = self.peek()
        expr = self.expression()
        end = self.expect(";")
        return Assign(target.text.upper(), expr, self.span(start, end), target.line, target.column)

    def call(self):
        instance = self.take()
        self.expect("(")
        params = []
        if not self.accept(")"):
            while True:
                name = self.name()
                self.expect(":=")
                start = self.peek()
                expr = self.expression()
                params.append((name.text.upper(), expr, self.span(start, self.peek()), name))
                if self.accept(")"):
                    break
                self.expect(",")
        self.expect(";")
        return Call(instance.text.upper(), params, instance.line, instance.column)

    def if_statement(self):
        first = self.expect("IF")
        branches = []
        start = self.peek()
        condition = self.expression()
        then = self.expect("THEN")
        branches.append((condition, self.span(start, then), self.statements({"ELSIF", "ELSE", "END_IF"})))
        while self.accept("ELSIF"):
            start = self.peek()
            condition = self.expression()
            then = self.expect("THEN")
            branches.append((condition, self.span(start, then), self.statements({"ELSIF", "ELSE", "END_IF"})))
        otherwise = self.statements({"END_IF"}) if self.accept("ELSE") else None
        self.expect("END_IF")
        self.expect(";")
        return If(branches, otherwise, first.line, first.column)

    # expressions, lowest precedence first (Bolton Table 6.3, p. 168)
    def expression(self):
        return self.binary(0)

    LEVELS = [("OR",), ("XOR",), ("AND", "&"), ("=", "<>"), ("<", ">", "<=", ">="), ("+", "-"), ("*", "/", "MOD")]

    def binary(self, level):
        if level == len(self.LEVELS):
            return self.unary()
        left = self.binary(level + 1)
        while self.peek().kind in ("OP", "KEYWORD") and self.peek().text in self.LEVELS[level]:
            op = self.take()
            right = self.binary(level + 1)
            name = "AND" if op.text == "&" else op.text
            left = Binary(op.line, op.column, op=name, left=left, right=right)
        return left

    def unary(self):
        token = self.peek()
        if self.accept("-") or self.accept("NOT"):
            return Unary(token.line, token.column, op=token.text, operand=self.unary())
        return self.power()

    def power(self):
        left = self.primary()
        while self.peek().text == "**" and self.peek().kind == "OP":
            op = self.take()
            left = Binary(op.line, op.column, op="**", left=left, right=self.primary())
        return left

    def primary(self):
        token = self.take()
        if token.kind == "OP" and token.text == "(":
            expr = self.expression()
            self.expect(")")
            return expr
        if token.kind in ("INT", "REAL", "TIME"):
            return Literal(token.line, token.column, value=token.value, type=token.kind)
        if token.kind == "KEYWORD" and token.text in ("TRUE", "FALSE"):
            return Literal(token.line, token.column, value=token.text == "TRUE", type="BOOL")
        if token.kind == "NAME":
            if self.accept("."):
                member = self.name()
                return Member(token.line, token.column, instance=token.text.upper(), field=member.text.upper())
            if self.peek().text == "(":
                raise PlcError("UNSUPPORTED_SYNTAX", "Function calls inside expressions are outside the subset",
                               token.line, token.column)
            return Name(token.line, token.column, key=token.text.upper())
        raise PlcError("SYNTAX", f"Unexpected {token.text or 'end of program'} in expression",
                       token.line, token.column)


class _Checker:
    """Static types (spec section 4). Every node gets .type; errors name line and column."""

    def __init__(self, program: Program):
        self.decls = program.decls

    def check(self, program):
        self.body(program.body)

    def body(self, statements):
        for statement in statements:
            if isinstance(statement, Assign):
                decl = self.decl(statement.target, statement.line, statement.column)
                if decl.type in BLOCKS:
                    raise PlcError("TYPE_MISMATCH", f"{decl.name} is a function block; call it instead",
                                   statement.line, statement.column)
                if decl.section == "input":
                    raise PlcError("READ_ONLY", f"{decl.name} is an input; the program cannot write it",
                                   statement.line, statement.column)
                value = self.expr(statement.expr)
                if not (value == decl.type or (decl.type == "REAL" and value == "INT")):
                    raise PlcError("TYPE_MISMATCH", f"Cannot assign {value} to {decl.name} ({decl.type})",
                                   statement.line, statement.column)
            elif isinstance(statement, If):
                for condition, _, branch in statement.branches:
                    if self.expr(condition) != "BOOL":
                        raise PlcError("TYPE_MISMATCH", "IF and ELSIF conditions must be BOOL",
                                       condition.line, condition.column)
                    self.body(branch)
                if statement.otherwise is not None:
                    self.body(statement.otherwise)
            else:
                decl = self.decl(statement.instance, statement.line, statement.column)
                if decl.type not in BLOCKS:
                    raise PlcError("TYPE_MISMATCH", f"{decl.name} is not a function block",
                                   statement.line, statement.column)
                inputs = BLOCKS[decl.type][0]
                seen = set()
                for name, expr, _, token in statement.params:
                    if name not in inputs:
                        raise PlcError("UNKNOWN_NAME", f"{decl.type} has no input {token.text}",
                                       token.line, token.column)
                    if name in seen:
                        raise PlcError("DUPLICATE_NAME", f"Input {token.text} is given twice", token.line, token.column)
                    seen.add(name)
                    if self.expr(expr) != inputs[name]:
                        raise PlcError("TYPE_MISMATCH", f"{decl.type}.{name} needs {inputs[name]}",
                                       expr.line, expr.column)

    def decl(self, key, line, column):
        if key not in self.decls:
            raise PlcError("UNKNOWN_NAME", f"{key} is not declared", line, column)
        return self.decls[key]

    def expr(self, node) -> str:
        node.type = self._type(node)
        return node.type

    def _type(self, node):
        if isinstance(node, Literal):
            if node.type == "INT" and not -32768 <= node.value <= 32768:
                raise PlcError("INT_OVERFLOW", f"{node.value} is outside INT", node.line, node.column)
            return node.type
        if isinstance(node, Name):
            decl = self.decl(node.key, node.line, node.column)
            if decl.type in BLOCKS:
                raise PlcError("TYPE_MISMATCH", f"{decl.name} is a function block; read one of its outputs",
                               node.line, node.column)
            return decl.type
        if isinstance(node, Member):
            decl = self.decl(node.instance, node.line, node.column)
            outputs = BLOCKS.get(decl.type, ({}, {}))[1]
            if node.field not in outputs:
                raise PlcError("UNKNOWN_NAME", f"{decl.name}.{node.field} is not an output of {decl.type or 'a block'}",
                               node.line, node.column)
            return outputs[node.field]
        if isinstance(node, Unary):
            operand = self.expr(node.operand)
            if node.op == "NOT" and operand == "BOOL":
                return "BOOL"
            if node.op == "-" and operand in ("INT", "REAL", "TIME"):
                return operand
            raise PlcError("TYPE_MISMATCH", f"{node.op} cannot apply to {operand}", node.line, node.column)
        left, right = self.expr(node.left), self.expr(node.right)
        op = node.op
        numeric = {"INT", "REAL"}
        if op in ("AND", "OR", "XOR"):
            if left == right == "BOOL":
                return "BOOL"
        elif op in ("=", "<>"):
            if left == right or {left, right} <= numeric:
                return "BOOL"
        elif op in ("<", ">", "<=", ">="):
            if (left == right and left != "BOOL") or {left, right} <= numeric:
                return "BOOL"
        elif op in ("+", "-"):
            if left == right == "TIME":
                return "TIME"
            if {left, right} <= numeric:
                return "INT" if left == right == "INT" else "REAL"
        elif op in ("*", "/"):
            if {left, right} <= numeric:
                return "INT" if left == right == "INT" else "REAL"
        elif op == "MOD":
            if left == right == "INT":
                return "INT"
        elif op == "**":
            if {left, right} <= numeric:
                return "REAL"
        raise PlcError("TYPE_MISMATCH", f"{op} cannot combine {left} and {right}", node.line, node.column)


def parse(source: str) -> Program:
    """Parse and type-check a program; raises PlcError with line and column."""
    program = _Parser(source).program()
    _Checker(program).check(program)
    return program
