
class PriorityQueue:
    def __init__(self):
        self.items = [None]

    def __repr__(self):
        return f"{self.items}"

    def size(self):
        return len(self.items) - 1

    def swap_items(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]
        self.items[i].heap_index = i
        self.items[j].heap_index = j

    def repair_heap_upwards(self, i):
        while i > 1:
            if self.items[i].key < self.items[i // 2].key:
                self.swap_items(i, i // 2)
            else:
                break
            i = i // 2

    def delete_min(self):
        if self.size() > 1:
            self.swap_items(1, self.size())
            self.items.pop()
            self.repair_heap_downwards(1)
            return

        if self.size() == 1:
            self.items.pop()
            return

    def repair_heap_downwards(self, i):
        while True:
            if 2*i + 1 <= self.size():
                if self.items[2*i].key < self.items[2*i+1].key:
                    self.swap_items(i, 2*i)
                    i = 2*i
                else:
                    self.swap_items(i, 2*i+1)
                    i = 2*i+1
            else:
                if 2*i == self.size():
                    if self.items[i].key > self.items[2*i].key:
                        self.swap_items(i, 2*i)
                        return
                return

    def insert(self, item):
        self.items.append(item)
        item.heap_index = self.size()
        self.repair_heap_upwards(item.heap_index)

    def get_min(self):
        if self.size() == 0:
            return None
        return self.items[1]

    def change_key(self, item: 'PriorityQueueItem'):
        if self.size() >= 2*item.heap_index+1:
            if item.key > self.items[2*item.heap_index].key or item.key > self.items[2*item.heap_index+1].key:
                self.repair_heap_downwards(item.heap_index)
                return

        if self.size() == 2*item.heap_index:
            if item.key > self.items[2*item.heap_index].key:
                self.repair_heap_downwards(item.heap_index)
                return
        if 1 >= item.heap_index // 2:
            if self.items[item.heap_index // 2] is None:
                return
            if item.key < self.items[item.heap_index//2].key:
                self.repair_heap_upwards(item.heap_index)
                return

    def remove(self, item: 'PriorityQueueItem'):
        if item.heap_index < self.size():
            self.swap_items(item.heap_index, self.size())
            self.items.pop()
            self.change_key(item)
            return
        if self.size() == 1:
            self.items.pop()
            return


class PriorityQueueItem:
    def __init__(self, key, value, heap_index: int = None):
        self.key = key
        self.value = value
        self.heap_index = heap_index

    def __repr__(self):
        return f"{self.key}{self.value}@{self.heap_index}"
