import math


#            2
#           / \
#          /   \
#         4     5
#        / \   / \
#       8   6 9   7
#      /\  /\ /\  /\
#    10 30 24
#
#   [2, 4, 5, 8, 6, 9, 7, 10, 30, 24]
#    0  1  2  3  4  5  6   7   8   9
#

def parent(i: int):
    parent_index = math.floor((i - 1) / 2)
    return parent_index


def left(i: int):
    left_index = i * 2 + 1
    return left_index


def right(i: int):
    right_index = i * 2 + 2
    return right_index


class MinHeap:
    def __init__(self):
        # self._internal_array = [2, 4, 5, 8, 6, 9, 7, 10, 30, 24]
        self._internal_array = [30, 10, 2, 8, 6, 5, 24, 4, 7, 9, 15, 31, 16, 3]

    def __str__(self):
        return str(self._internal_array)

    def size(self):
        return len(self._internal_array)

    def value(self, i: int):
        if i >= self.size():
            return None
        return self._internal_array[i]

    def swap(self, i, j):
        buf = self.value(i)
        self._internal_array[i] = self.value(j)
        self._internal_array[j] = buf
        print(f"{self._internal_array}  (swapped {self.value(i)} and {self.value(j)})")

    def sink_down(self, i: int):
        li = left(i)
        ri = right(i)
        if li < self.size() and self.value(li) < self.value(i):
            index_min = li
        else:
            index_min = i
        if ri < self.size() and self.value(ri) < self.value(index_min):
            index_min = ri

        if index_min != i:
            self.swap(i, index_min)
            self.sink_down(index_min)

    def swim_up(self, i: int):
        pi = parent(i)
        while i > 1 and self.value(pi) > self.value(i):
            self.swap(i, pi)
            i = pi
            pi = parent(i)

    def build_heap(self):
        i = math.floor(self.size() / 2)
        while i >= 0:
            print(f"Testing {self.value(i)} (index {i}) to see if it needs to sink")
            self.sink_down(i)
            i -= 1

    def insert(self, value: int):
        self._internal_array.append(value)
        print(f"Inserting {value} at tail, see if it needs to swim up")
        self.swim_up(self.size() - 1)

    def extract_min(self):
        res = self.value(0)
        self._internal_array[0] = self._internal_array[self.size() - 1]
        self._internal_array.pop()
        print(f"Extracting first index and putting {self.value(0)} at root. Test if it needs to sink")
        self.sink_down(0)
        return res
