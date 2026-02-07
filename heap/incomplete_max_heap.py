class MaxHeap:
    def __init__(self):
        # List to store heap elements
        # child of i is 2i+1 and 2i+2
        # parent of i is (i-1)//2
        self._list = []

    # Helper function to maintain the heap property
    def heapify(self, idx):
        max_idx = idx
        lc_idx = 2 * idx + 1
        rc_idx = 2 * idx + 2
        heap_size = len(self._list)

        if lc_idx < heap_size and self._list[lc_idx] > self._list[max_idx]:
            max_idx = lc_idx

        if rc_idx < heap_size and self._list[rc_idx] > self._list[max_idx]:
            max_idx = rc_idx

        if max_idx != idx:
            # swap
            self._list[idx], self._list[max_idx] = (
                self._list[max_idx],
                self._list[idx],
            )
            self.heapify(max_idx)

    # Function to insert a new key into the heap
    def insert(self, key):
        """
        Time Complexity: O(log N)
        """

        self._list.append(key)
        idx = len(self._list) - 1

        parent_idx = (idx - 1) // 2
        while (
            parent_idx >= 0 and self._list[parent_idx] < self._list[idx]
        ):  # Ensures You don’t go above the root
            self._list[idx], self._list[parent_idx] = (
                self._list[parent_idx],
                self._list[idx],
            )  # swaps
            idx = parent_idx
            parent_idx = (idx - 1) // 2

    # Function to extract the maximum element from the heap
    def extractMax(self):
        """
        Time Complexity: O(log N)
        """

        if len(self._list) <= 0:
            raise IndexError("Heap underflow")

        if len(self._list) == 1:
            return self._list.pop()

        root_value = self._list[0]
        self._list[0] = self._list.pop()
        self.heapify(0)

        return root_value

    # Function to get the maximum element from the heap
    def getMax(self):
        """
        Time Complexity: O(1)
        """

        if len(self._list) <= 0:
            raise IndexError("Heap is empty")
        return self._list[0]

    # Function to delete a key at a given index
    def deleteKey(self, index):
        """
        Time Complexity: O(log N)
        """

        if index >= len(self._list):
            raise IndexError("Invalid index")

        if index == len(self._list) - 1:
            self._list.pop()
        else:
            self._list[index] = self._list.pop()
            if index < len(self._list):
                self.heapify(index)

    # Function to increase the value of a key at a given index
    def increaseKey(self, idx, new_value):
        """
        Time Complexity: O(log N)
        """

        if idx >= len(self._list) or self._list[idx] >= new_value:
            raise ValueError("Invalid index or new value is not greater")

        self._list[idx] = new_value

        # since increased, hence no impact on children

        parent_index = (idx - 1) // 2
        while parent_index >= 0 and self._list[(idx - 1) // 2] < self._list[idx]:
            self._list[idx], self._list[parent_index] = (
                self._list[parent_index],
                self._list[idx],
            )
            idx = parent_index
            parent_index = (idx - 1) // 2

    # Function to print the heap elements
    def printHeap(self):
        print(*self._list)


# h = MaxHeap()
# h.insert(1)
# h.insert(2)
# h.insert(3)
# h.insert(4)
# h.insert(5)
# h.printHeap()
# h.deleteKey(2)
# h.printHeap()

# # print(h.extractMax())
# # print(h.extractMax())
# # print(h.extractMax())
# # print(h.extractMax())
# # print(h.extractMax())



heap = MaxHeap()
for x in [50, 30, 40, 10, 20]:
    heap.insert(x)
    heap.printHeap()

heap.deleteKey(1) 
heap.printHeap()