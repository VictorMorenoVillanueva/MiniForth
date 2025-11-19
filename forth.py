# forth.py

from antlr4 import InputStream, CommonTokenStream

from forthLexer import forthLexer
from forthParser import forthParser
from machine import Machine
from visitor_user import ForthExecutor


def interpret(code: str):
    """
    Interpreta un programa mini-Forth passat com string.
    Retorna l'últim valor mostrat (. o .s), si n'hi ha.
    """
    input_stream = InputStream(code)
    lexer = forthLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = forthParser(token_stream)

    tree = parser.program()

    machine = Machine()
    executor = ForthExecutor(machine)
    executor.visit(tree)
    return None
