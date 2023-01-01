import sys
import collections


def parse_input_line(line):
    v, adj = line.split(' <-> ')
    v = int(v)
    adj = [int(w) for w in adj.split(', ')]
    return (v, adj)


def build_adj_list_graph(N, lines):
    edges = [[] for _ in range(N)]
    for line in lines:
        v, adj = parse_input_line(line)
        for w in adj:
            edges[v].append(w)
    
    return edges


BIG = 1 << 40

def bfs(graph, source, checked):
    N = len(graph)
    distance = [BIG] * N
    queue = collections.deque()

    def visit(v, d):
        if distance[v] > d:
            checked[v] = True
            distance[v] = d
            queue.append(v)
    
    visit(source, 0)
    while queue:
        v = queue.popleft()
        for w in graph[v]:
            visit(w, distance[v] + 1)
    
    return distance


def main():
    lines = [line.strip() for line in sys.stdin.readlines()]

    N = 2000
    checked = [False] * N
    graph = build_adj_list_graph(N, lines)
    distance = bfs(graph, 0, checked)

    # part 1
    print(sum(distance[x] < BIG for x in range(N)))

    # part 2
    groups = 1
    for i in range(1, N):
        if not checked[i]:
            bfs(graph, i, checked)
            groups += 1
    print(groups)


main()