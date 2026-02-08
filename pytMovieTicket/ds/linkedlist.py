class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    """Singly linked list preserves insertion order for selected seats."""
    def __init__(self):
        self.head = None
        self.tail = None
        self._len = 0

    def add(self, value):
        node = LinkedListNode(value)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._len += 1

    def remove(self, value):
        prev = None
        cur = self.head
        while cur:
            if cur.value == value:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                if cur == self.tail:
                    self.tail = prev
                self._len -= 1
                return True
            prev = cur
            cur = cur.next
        return False

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def clear(self):
        self.head = None
        self.tail = None
        self._len = 0

    def contains(self, value):
        cur = self.head
        while cur:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def __len__(self):
        return self._len
