class Stack:
    def __init__(self):
        self._s = []

    def push(self, x):
        self._s.append(x)

    def pop(self):
        if self._s:
            return self._s.pop()
        return None

    def peek(self):
        if self._s:
            return self._s[-1]
        return None

    def is_empty(self):
        return len(self._s) == 0

    def size(self):
        return len(self._s)
