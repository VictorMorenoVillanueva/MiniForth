# forth.py

from antlr4 import InputStream, CommonTokenStream

from forthLexer import forthLexer
from forthParser import forthParser
from machine import Machine
from visitor_user import ForthExecutor


def interpret(code: str) -> None:
    """Intèrpret de mini Forth. Rep un string i executa el programa."""
    input_stream = InputStream(code)
    lexer = forthLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = forthParser(tokens)
    tree = parser.program()

    machine = Machine()
    executor = ForthExecutor(machine)
    executor.visit(tree)


