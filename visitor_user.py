from forthVisitor import forthVisitor as AntlrForthVisitor
from machine import Machine


class ForthExecutor(AntlrForthVisitor):

    def __init__(self, machine: Machine):
        super().__init__()
        self.m = machine
        self.words = {}
        self.call_stack = []

        # Operadors binaris de tipus a op b
        self.binary_ops = {
            '+':  lambda a, b: a + b,
            '-':  lambda a, b: a - b,
            '*':  lambda a, b: a * b,
            '/':  self._safe_div,
            'mod': self._safe_mod,
        }

        # Relacionals → retornen 0 o -1
        self.rel_ops = {
            '<':  lambda a, b: -1 if a < b else 0,
            '<=': lambda a, b: -1 if a <= b else 0,
            '>':  lambda a, b: -1 if a > b else 0,
            '>=': lambda a, b: -1 if a >= b else 0,
            '=':  lambda a, b: -1 if a == b else 0,
            '<>': lambda a, b: -1 if a != b else 0,
        }

        # Booleans → retornen 0 o -1
        self.bool_ops = {
            'and': lambda a, b: -1 if (a != 0 and b != 0) else 0,
            'or':  lambda a, b: -1 if (a != 0 or b != 0) else 0,
        }

    # ---------------------------
    # Funcions auxiliars
    # ---------------------------

    def _pop2(self):
        """Extreu dos valors comprovant pila."""
        b = self.m.pop()
        a = self.m.pop()
        if a is None or b is None:
            return None, None
        return a, b

    def _safe_div(self, a, b):
        if b == 0:
            print("Error: divisió per zero!")
            return 0
        return a // b

    def _safe_mod(self, a, b):
        if b == 0:
            print("Error: divisió per zero!")
            return 0
        return a % b

    # ---------------------------
    # Execució de paraules
    # ---------------------------

    def visitProgram(self, ctx):
        for elem in ctx.element():
            self.visit(elem)
        return None

    def visitDefinition(self, ctx):
        self.words[ctx.IDENT().getText()] = list(ctx.instruction())
        return None

    def _execute_word(self, name):
        body = self.words.get(name)
        if body is None:
            print(f"Error: paraula '{name}' no definida!")
            return
        self.call_stack.append(name)
        try:
            for instr in body:
                self.visit(instr)
        finally:
            self.call_stack.pop()

    # ---------------------------
    # Instruccions
    # ---------------------------

    def visitNumberInstr(self, ctx):
        self.m.push(int(ctx.NUMBER().getText()))
        return None

    def visitCallInstr(self, ctx):
        self._execute_word(ctx.IDENT().getText())
        return None

    def visitBuiltinInstr(self, ctx):
        t = ctx.builtin().start.text
        m = self.m

        # Aritmètica
        if t in self.binary_ops:
            a, b = self._pop2()
            if a is not None:
                m.push(self.binary_ops[t](a, b))
            return None

        # Relacionals
        if t in self.rel_ops:
            a, b = self._pop2()
            if a is not None:
                m.push(self.rel_ops[t](a, b))
            return None

        # Booleans binaris
        if t in self.bool_ops:
            a, b = self._pop2()
            if a is not None:
                m.push(self.bool_ops[t](a, b))
            return None

        # Boolean unari: not
        if t == 'not':
            a = m.pop()
            if a is not None:
                m.push(0 if a != 0 else -1)
            return None

        # Sortida
        if t == '.':
            m.print_top()
            return None
        if t == '.s':
            m.show_stack()
            return None

        # Manipulació de la pila
        if t == 'swap':
            a, b = self._pop2()
            if a is not None:
                m.push(b)
                m.push(a)
            return None

        if t == '2swap':
            if len(m.stack) < 4:
                print("Error: pila buida!")
                return None
            a, b, c, d = m.stack[-4:]
            m.stack[-4:] = [c, d, a, b]
            return None

        if t == 'dup':
            a = m.peek()
            if a is not None:
                m.push(a)
            return None

        if t == '2dup':
            if len(m.stack) < 2:
                print("Error: pila buida!")
                return None
            a, b = m.stack[-2:]
            m.push(a)
            m.push(b)
            return None

        if t == 'over':
            if len(m.stack) < 2:
                print("Error: pila buida!")
                return None
            m.push(m.stack[-2])
            return None

        if t == '2over':
            if len(m.stack) < 4:
                print("Error: pila buida!")
                return None
            a, b = m.stack[-4], m.stack[-3]
            m.push(a)
            m.push(b)
            return None

        if t == 'rot':
            if len(m.stack) < 3:
                print("Error: pila buida!")
                return None
            a, b, c = m.stack[-3:]
            m.stack[-3:] = [b, c, a]
            return None

        if t == 'drop':
            m.pop()
            return None

        if t == '2drop':
            m.pop()
            m.pop()
            return None

        # Recursivitat
        if t == 'recurse':
            if self.call_stack:
                self._execute_word(self.call_stack[-1])
            return None

        return None

    # ---------------------------
    # If / Else / Endif
    # ---------------------------

    def visitIfInstr(self, ctx):
        cond = self.m.pop()
        branch = ctx.trueBranch if cond != 0 else ctx.falseBranch
        if branch:
            for instr in branch:
                self.visit(instr)
        return None
