class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.previous = None

    def add(self, node):
        if self.head == None:
            self.head = node
        else:
            self.previous.next = node
        self.previous = node

    def display(self):
        temp = self.head
        out_list = []
        while(temp):
            out_list.append(temp.data)
            temp = temp.next
        print(" -> ".join(map(str, out_list)))

    def reverse(self):
        previous_node = None
        current_node= self.head
        next_node = None

        while(current_node):
            next_node = current_node.next
            current_node.next = previous_node
            previous_node = current_node
            current_node = next_node
        self.head = previous_node

    def findloop(self):
        slow = self.head
        fast = self.head.next


if __name__ == '__main__':

    # creating the nodes
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)

    # adding nodes to the linked list
    linked_list = LinkedList()
    linked_list.add(n1)
    linked_list.add(n2)
    linked_list.add(n3)
    linked_list.add(n4)
    linked_list.add(n5)

    # display linked list
    linked_list.display()

    # reverse the linked list and display
    linked_list.reverse()
    linked_list.display()
