# machine.py

class Machine:
    def __init__(self):
        self.stack = []
        self.last_output = None

    def push(self, value: int) -> None:
        self.stack.append(value)

    def pop(self):
        """Extreu el cim de la pila. Si està buida, mostra l'error."""
        if not self.stack:
            print("Error: pila buida!")
            return None
        return self.stack.pop()

    def peek(self):
        """Mira el cim de la pila sense extreure'l."""
        if not self.stack:
            print("Error: pila buida!")
            return None
        return self.stack[-1]

    def print_top(self) -> None:
        """Implementació de '.'"""
        value = self.pop()
        if value is None:
            # ja s'ha imprès l'error, no imprimim res més
            return
        print(value)
        self.last_output = value

    def show_stack(self) -> None:
        """Implementació de '.s'"""
        print(self.stack)
        self.last_output = list(self.stack)
