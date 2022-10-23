class FIFOQueue:
    def __init__(self):
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None
    def is_empty(self):
        return len(self.queue) == 0
    def __str__(self):
        return str(self.queue)