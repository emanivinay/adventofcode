import collections


def read_input():
  return [input().strip() for _ in range(100)]


def add(y, x, queue, size_array, checked):
  if 0 <= y < N and 0 <= x < N and not checked[y][x] and cave[y][x] != '9':
    queue.append((y, x))
    checked[y][x] = True
    size_array[0] += 1


def main():
  cave = read_input()
  N = 100

  checked = [[False] * N for _ in range(N)]
  basin_sizes = []

  NEIGHBORS = [(1, 0), (0, 1), (0, -1), (-1, 0)]

  for y in range(N):
    for x in range(N):
      if not checked[y][x]:
        size = [0]
        queue = collections.deque()
        add(y, x, queue, size, checked)
        while queue:
          y, x = queue.popleft()
          for dy, dx in NEIGHBORS:
            y2, x2 = y + dy, x + dx
            add(y2, x2, queue, size, checked)
        
        basin_sizes.append(size[0])
  
  basin_sizes.sort()
  print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])


if __name__ == '__main__':
  main()
