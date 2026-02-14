# -----------------------------------------
# XOR Linked List Implementation in Python
# -----------------------------------------


from typing import Dict


class Node:
    def __init__(self, data):
        self.data = data

        # This will store XOR of prev and next node addresses
        # default = 0 ==> [as no prev and no next as of now, so id(None)^id(None)=0]
        self.PxN = 0  # id(None) ^ id(None)


class XORLinkedList_WithExplicitNoneAddress:
    def __init__(self):
        self.head = None
        self.tail = None

        """
        Note:
            In Python, even though id(obj) returns the object's memory address (in CPython),
            we cannot dereference that address like C/C++ using *p.
            Python does not allow direct pointer access, so we must maintain
            a mapping (address -> Node) to simulate pointer behavior.
        """
        self.__nodes: Dict[int, Node] = {
            id(None): None,
        }

    def _get_obj(self, _id):
        """Helper method to get object from address"""
        return self.__nodes.get(_id)

    def add(self, data):
        """Add node at the end"""
        new_node = Node(data)

        # Store node in dictionary
        self.__nodes[id(new_node)] = new_node

        if self.head is None:  # If list is empty
            self.head = self.tail = new_node
            # bcz it is alone, no prev and no next as of now, so id(None)^id(None)=0

        # elif self.head == self.tail:  # else if only one node is there

        #     self.tail.PxN ^= id(None)^id(new_node)  # tail.next is new_node
        #     new_node.PxN ^= id(self.tail)^id(None)  # new_node.prev is tail
        #     self.tail = new_node  # tail now points to new_node
        else:
            self.tail.PxN ^= id(None) ^ id(new_node)  # tail.next is new_node
            new_node.PxN ^= id(self.tail) ^ id(None)  # new_node.prev is tail
            self.tail = new_node  # tail now points to new_node

    # Traverse and print list
    def print_list(self):
        prev = None
        current = self.head

        print("XOR Linked List:", end=" ")
        while current:
            print(current.data, end=" -> ")

            next_id = current.PxN ^ id(prev)
            prev, current = current, self._get_obj(next_id)

        print("None")

    def print_reverse_list(self):
        next = None
        current = self.tail
        print("XOR Linked List (Reversed):", end=" ")
        print("None", end="")
        while current:
            print(f" <- {current.data}", end="")
            prev_id = current.PxN ^ id(next)
            current, next = self._get_obj(prev_id), current

        print()


class XORLinkedList_WithNoneAddressAsZero:
    def __init__(self):
        self.head = None
        self.tail = None

        self.__nodes: Dict[int, Node] = dict()

    def _get_obj(self, _id):
        # since we know python never alocates anything at address 0,
        # so we are safe to assume id(None) = 0
        # and this method will always return `None` when _id = 0
        return self.__nodes.get(_id)

    def add(self, data):

        new_node = Node(data)
        self.__nodes[id(new_node)] = new_node

        if self.head is None:  # If list is empty
            self.head = self.tail = new_node
        else:
            self.tail.PxN ^= id(new_node)
            new_node.PxN ^= id(self.tail)
            self.tail = new_node

    # Traverse and print list
    def print_list(self):
        prev = None
        current = self.head

        print("XOR Linked List:", end=" ")

        while current:
            print(current.data, end=" -> ")

            next_id = current.PxN ^ (id(prev) if prev else 0)
            prev, current = current, self._get_obj(next_id)

        print("None")

    def print_reverse_list(self):
        next = None
        current = self.tail

        print("XOR Linked List (Reversed):", end=" ")

        print("None", end="")
        while current:
            print(f" <- {current.data}", end="")
            prev_id = current.PxN ^ (id(next) if next else 0)
            current, next = self._get_obj(prev_id), current

        print()


# -----------------------
# Example Usage
# -----------------------


def _explicit_none_address_test():
    xor_list = XORLinkedList_WithExplicitNoneAddress()

    xor_list.add(10)
    xor_list.add(20)
    xor_list.add(30)
    xor_list.add(40)

    xor_list.print_list()
    xor_list.print_reverse_list()
    print()


def _none_address_as_zero_test():
    xor_list = XORLinkedList_WithNoneAddressAsZero()

    xor_list.add(10)
    xor_list.add(20)
    xor_list.add(30)
    xor_list.add(40)

    xor_list.print_list()
    xor_list.print_reverse_list()
    print()


if __name__ == "__main__":
    _explicit_none_address_test()
    _none_address_as_zero_test()
