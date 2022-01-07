from collections import defaultdict

def main():
  edges = defaultdict(list)
  for _ in range(23):
    a, b = input().split('-')
    edges[a].append(b)
    edges[b].append(a)
  
  visited = defaultdict(int)

  def f(node):
    if node == 'end':
      return 1
    
    if node.islower():
      if visited[node] != 0 and (node == 'start' or max(visited.values()) >= 2):
          return 0
      visited[node] += 1

    ret = sum(f(next) for next in edges[node])

    if node.islower():
      visited[node] -= 1
    
    return ret
  
  print(f('start'))

main()
