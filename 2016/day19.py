class DoublyLinkedList:
    def __init__(self):
        pass

    def remove(self, node):
        pass


class Player:
    def __init__(self, index, value):
        self.value = value
        self.index = index
        self.next = None
        self.prev = None
    
    def clear(self):
        self.value = 0
        self.next = self.prev = None


class Circle:
    def __init__(self, n):
        self.head = self.tail = Player(1, 1)
        for i in range(1, n):
            new_node = Player(i + 1, 1)
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        
        self.cur = self.head
    
    def get_next_to_player(self, player):
        return self.head if player is self.tail else player.next

    def steal_and_kick_next_player_out(self):
        next_player = self.get_next_to_player(self.cur)
        self.cur.value += next_player.value
        self.cur = self.get_next_to_player(next_player)
        if next_player is self.head:
            self.head = next_player.next
            self.head.prev = None
        elif next_player is self.tail:
            self.tail = next_player.prev
            self.tail.next = None
        else:
            prev = next_player.prev
            next = next_player.next
            prev.next = next
            next.prev = prev

        next_player.clear()


def main():
    N = 3017957
    circle = Circle(N)

    for i in range(N - 1):
        circle.steal_and_kick_next_player_out()

    # part 1    
    print(circle.head.index)


if __name__ == '__main__':
    main()
