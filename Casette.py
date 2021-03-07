"""
FelipedelosH 
2021


"""
class Node:
    def __init__(self):
        """
        This is a simple list with double link
        """
        self.previuos = None
        self.data = None
        self.next = None


class Casette:
    def __init__(self):
        """
        This is a universe container, and do next and previus action
        """
        self.tape = Node() # Containt all information
        self.name = ""
        self.duration = 0 # Count nodes

    def addData(self, x):
        """
        Register a data here
        """
        if self.tape.data == None:
            self.tape.data = x
            self.duration = 1
        else:
            node = self.tape

            while node.next != None:
                node = node.next

            node.next = Node()
            node.next.data = x
            self.duration = self.duration + 1


    def getData(self, x):
        """
        Return a pos x to the tape
        """
        if self.duration > x:
            count = 0
            temp = self.tape
            
            while count != x:
                temp =temp.next
                count = count + 1

            return temp.data
        else:
            return None

    def deteleAll(self):
        self.tape = Node()
        self.duration = 0

    def printList(self):
        temp = self.tape

        for i in range(0, self.duration):
            print(temp.data)
            temp = temp.next