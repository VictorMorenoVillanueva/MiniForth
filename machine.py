class Machine:
    def __init__(self):
        self.stack = []
        self.last_output = None

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.stack:
            print("Error: pila buida!")
            return None
        return self.stack.pop()

    def peek(self):
        if not self.stack:
            print("Error: pila buida!")
            return None
        return self.stack[-1]

    def print_top(self):
        value = self.pop()
        if value is None:
            return
        print(value)
        self.last_output = value

    def show_stack(self):
        print(self.stack)
        self.last_output = list(self.stack)
