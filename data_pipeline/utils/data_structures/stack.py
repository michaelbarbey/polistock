# Last-in First-out: stack implementation
# pushes each search into a history stack, allows to return to a previous seach
class Stack:
    def __init__(self):
        # underlying list to hold items
        self._items = []

    def push(self, item):
        # push onto the top of the stack
        self._items.append(item)

    def pop(self):
        # pop the top item, or return None if empty
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        # look at the top without removing
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        # True if no items
        return len(self._items) == 0

    def size(self):
        # optional helper
        return len(self._items)