#!/usr/bin/env pipenv run python
'''
file:           binary_heap.py
author:         Max Legrand
lastChangedBy:  Max Legrand
fileOverview:   Class file for binary heap
'''


class BinaryHeap:
    """
    Class file for BinaryHeap
    """

    def __init__(self):
        """
        Initialize array and set size to 0
        """
        super().__init__()
        self.heap_array = [(-1, (-1, -1))]
        self.size = 0

    def heapify_up(self, index):
        """
        Re-build heap moving upwards

        Args:
            index (int): index to start rebuilding at
        """
        while index // 2 > 0:
            if self.heap_array[index][0] < self.heap_array[index // 2][0]:
                temp = self.heap_array[index // 2]
                self.heap_array[index // 2] = self.heap_array[index]
                self.heap_array[index] = temp
            index = index // 2

    def insert(self, item):
        """
        insert item into heap

        Args:
            item (tuple): tuple containing f value and location
        """
        self.heap_array.append(item)
        self.size = self.size + 1
        self.heapify_up(self.size)

    def heapify_down(self, index):
        """
        Re-build heap moving downwards

        Args:
            index (int): index to start rebuild at
        """
        while index*2 <= self.size:
            min_child = self.min_child(index)
            if self.heap_array[index][0] > self.heap_array[min_child][0]:
                temp = self.heap_array[index]
                self.heap_array[index] = self.heap_array[min_child]
                self.heap_array[min_child] = temp
            index = min_child

    def min_child(self, index):
        """
        Find minimum f-value child

        Args:
            index (int): index of current element

        Returns:
            int: index of minimum f-value child
        """
        if index*2+1 > self.size:
            return index*2
        if self.heap_array[index*2][0] < self.heap_array[index*2+1][0]:
            return index*2
        return index*2+1

    def delete_min(self):
        """
        Removes minimum f-value element from heap

        Returns:
            tuple: returns a tuple containing f-value and location in the
                   following format: (minimum f-value, (row, col))
        """
        returnval = self.heap_array[1]
        self.heap_array[1] = self.heap_array[self.size]
        self.size = self.size - 1
        self.heap_array.pop()
        self.heapify_down(1)
        return returnval

    def build_heap(self, h_list):
        """
        Builds heap from array

        Args:
            h_list (array): array of tuples of the following format: (f-value, (row, col))
        """
        index = len(h_list) // 2
        self.size = len(h_list)
        self.heap_array = [(-1, (-1, -1))] + h_list[:]
        while index > 0:
            self.heapify_down(index)
            index = index - 1


if __name__ == "__main__":
    # Test heap class
    heap = BinaryHeap()
    heap.build_heap([
        (9, (0, 0)),
        (5, (1, 2)),
        (6, (3, 3)),
        (2, (0, 1)),
        (4, (8, 1))
    ])
    print(heap.delete_min())
    print(heap.delete_min())
    print(heap.delete_min())
    print(heap.delete_min())
    print(heap.delete_min())
