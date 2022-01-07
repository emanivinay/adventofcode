class Board:
    def __init__(self, grid):
        self.grid = grid
        self.marked = [[False] * 5 for _ in range(5)]
        self._done = False

    def cross(self, number):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == number:
                    self.marked[i][j] = True
                    return

    def over(self):
        for i in range(5):
            if all(self.marked[i]) or all(self.marked[r][i] for r in range(5)):
                return True

        return False

    def done(self):
        prev = self._done
        if not self._done:
            self._done = self.over()
        return prev


def processInput():
    callingSeq = [int(word) for word in input().split(',')]

    boards = []
    for _ in range(100):
        input()
        boards.append(Board([[int(word) for word in input().split()] for _ in range(5)]))

    return (callingSeq, boards)


def main():
    seq, boards = processInput()
    for number in seq:
        for i in range(len(boards)):
            boards[i].cross(number)
            if boards[i].over():
                unmarkedSum = sum(value for r, row in enumerate(boards[i].grid)
                                            for col, value in enumerate(row)
                                            if not boards[i].marked[r][col])

                if not boards[i].done():
                    print(unmarkedSum * number)
    
main()
