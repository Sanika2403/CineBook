class Queue:
    def __init__(self):
        self._q = []

    def enqueue(self, x):
        self._q.append(x)

    def dequeue(self):
        if self._q:
            return self._q.pop(0)
        return None

    def is_empty(self):
        return len(self._q) == 0

    def size(self):
        return len(self._q)

    def to_list(self):
        return list(self._q)
