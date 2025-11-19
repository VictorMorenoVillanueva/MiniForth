# visitor_user.py

from forthVisitor import forthVisitor as AntlrForthVisitor
from machine import Machine


class ForthExecutor(AntlrForthVisitor):
    def __init__(self, machine: Machine):
        super().__init__()
        self.machine = machine
        self.words: dict[str, list] = {}   # nom -> llista d'instructions (ctx)
        self.call_stack: list[str] = []    # per a recurse

    # --- programes i definicions ---

    def visitProgram(self, ctx):
        for elem in ctx.element():
            self.visit(elem)
        return self.machine.last_output

    def visitDefinition(self, ctx):
        name = ctx.IDENT().getText()
        body = list(ctx.instruction())
        self.words[name] = body
        return None

    def _execute_word(self, name: str):
        body = self.words.get(name)
        if body is None:
            #print(f"Error: paraula '{name}' no definida!") <-- Això o no?
            return
        self.call_stack.append(name)
        try:
            for instr in body:
                self.visit(instr)
        finally:
            self.call_stack.pop()

    # --- instruccions bàsiques ---

    def visitNumberInstr(self, ctx):
        value = int(ctx.NUMBER().getText())
        self.machine.push(value)
        return None

    def visitCallInstr(self, ctx):
        name = ctx.IDENT().getText()
        self._execute_word(name)
        return None

    def visitBuiltinInstr(self, ctx):
        token_text = ctx.builtin().start.text
        m = self.machine

        # --- Aritmètica ---
        if token_text == '+':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(a + b)

        elif token_text == '-':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(a - b)

        elif token_text == '*':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(a * b)

        elif token_text == '/':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            if b == 0:
                print("Error: divisió per zero!")
                m.push(0)
            else:
                m.push(a // b)

        elif token_text == 'mod':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            if b == 0:
                print("Error: divisió per zero!")
                m.push(0)
            else:
                m.push(a % b)

        # --- Sortida ---
        elif token_text == '.':
            m.print_top()

        elif token_text == '.s':
            m.show_stack()

        # --- Manipulació de la pila ---

        elif token_text == 'swap':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(b)
            m.push(a)

        elif token_text == '2swap':
            d = m.pop()
            c = m.pop()
            b = m.pop()
            a = m.pop()
            if None in (a, b, c, d):
                return None
            m.push(c)
            m.push(d)
            m.push(a)
            m.push(b)

        elif token_text == 'dup':
            a = m.peek()
            if a is None:
                return None
            m.push(a)

        elif token_text == '2dup':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(a)
            m.push(b)
            m.push(a)
            m.push(b)

        elif token_text == 'over':
            # cal com a mínim 2 elements
            if len(m.stack) < 2:
                print("Error: pila buida!")
                return None
            a = m.stack[-2]
            m.push(a)

        elif token_text == '2over':
            # cal com a mínim 4 elements
            if len(m.stack) < 4:
                print("Error: pila buida!")
                return None
            a = m.stack[-4]
            b = m.stack[-3]
            m.push(a)
            m.push(b)

        elif token_text == 'rot':
            c = m.pop()
            b = m.pop()
            a = m.pop()
            if None in (a, b, c):
                return None
            m.push(b)
            m.push(c)
            m.push(a)

        elif token_text == 'drop':
            m.pop()

        elif token_text == '2drop':
            m.pop()
            m.pop()

        # --- Relacionals ---
        elif token_text == '<':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a < b else 0)

        elif token_text == '<=':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a <= b else 0)

        elif token_text == '>':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a > b else 0)

        elif token_text == '>=':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a >= b else 0)

        elif token_text == '=':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a == b else 0)

        elif token_text == '<>':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            m.push(-1 if a != b else 0)

        # --- Booleans ---
        elif token_text == 'and':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            a_true = (a != 0)
            b_true = (b != 0)
            m.push(-1 if (a_true and b_true) else 0)

        elif token_text == 'or':
            b = m.pop()
            a = m.pop()
            if a is None or b is None:
                return None
            a_true = (a != 0)
            b_true = (b != 0)
            m.push(-1 if (a_true or b_true) else 0)

        elif token_text == 'not':
            a = m.pop()
            if a is None:
                return None
            a_true = (a != 0)
            m.push(0 if a_true else -1)

        # --- Recursivitat ---
        elif token_text == 'recurse':
            if self.call_stack:
                self._execute_word(self.call_stack[-1])

        return None

    def visitIfInstr(self, ctx):
        """
        condició if codi_cert else codi_fals endif
        """
        cond = self.machine.pop()
        true_branch = (
            list(ctx.trueBranch)
            if ctx.trueBranch is not None
            else []
        )

        false_branch = (
            list(ctx.falseBranch)
            if ctx.falseBranch is not None
            else []
        )

        # qualsevol valor != 0 es tracta com a cert
        if cond != 0:
            for instr in true_branch:
                self.visit(instr)
        else:
            for instr in false_branch:
                self.visit(instr)

        return None
