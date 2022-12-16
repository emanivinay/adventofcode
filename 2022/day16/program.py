import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_input_line(line):
    tokens = line.split()
    node = tokens[1]
    outflow_rate = int(tokens[4].split('=')[1][:-1])
    if 'valves' in tokens:
        i = tokens.index('valves')
    else:
        i = tokens.index('valve')

    outgoing_edges = []
    for j in range(i + 1, len(tokens)):
        adj = tokens[j]
        if adj.endswith(','):
            adj = adj[:-1]
        outgoing_edges.append(adj)
    
    return (node, outflow_rate, outgoing_edges)


def main():
    input_lines = sys.stdin.read().split('\n')

    N = 0
    node_id_map = dict()
    def gid(node):
        nonlocal N
        if node in node_id_map:
            return node_id_map[node]
        
        node_id_map[node] = N
        N += 1
        return node_id_map[node]
    
    MAXN = 128
    flow_rates = [0] * MAXN
    graph = [[MAXN + 10] * MAXN for _ in range(MAXN)]
    for i in range(MAXN):
        graph[i][i] = 0

    positive_rate_nodes = []
    for line in input_lines:
        node, rate, edges = parse_input_line(line)
        flow_rates[gid(node)] = rate
        if rate > 0 or node == 'AA':
            positive_rate_nodes.append(gid(node))
        for adj_node in edges:
            graph[gid(node)][gid(adj_node)] = min(graph[gid(node)][gid(adj_node)], 1)

    M = len(positive_rate_nodes)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                graph[j][k] = min(graph[j][k], graph[j][i] + graph[i][k])


    def simulate(T):
        queue = collections.deque()
        best = collections.defaultdict(lambda: -1)
        
        aa = positive_rate_nodes.index(gid('AA'))
        def add(i, added, v, t):
            if t >= 0 and (best[(i, added, t)] < v):
                best[(i, added, t)] = v
                queue.append((i, t, added, v))
        
        add(aa, 0, 0, T)
        while queue:
            i, t, added, v = queue.popleft()
            if (added & (1 << i)) == 0 and t >= 1:
                flow_here = (t - 1) * flow_rates[positive_rate_nodes[i]]
                add(i, added | (1 << i), v + flow_here, t - 1)
            
            for j in range(M):
                t_move = graph[positive_rate_nodes[i]][positive_rate_nodes[j]]
                if t_move <= t:
                    add(j, added, v, t - t_move)
    
        return best

    best1 = simulate(30)
    print(max(best1.values()))

    best2 = simulate(26)
    # best => (end_node, mask_turned, time_left) => max_flow
    table = [0] * (1 << M)
    for (i, added, t), vmax in best2.items():
        table[added] = max(table[added], vmax)
    
    ret = 0
    for mask in range(1 << M):
        mask3 = ((1 << M) - 1) ^ mask
        ret = max(ret, table[mask3])
        mask2 = mask
        while mask2 > 0:
            ret = max(ret, table[mask3] + table[mask2])
            mask2 = (mask2 - 1) & mask

    print(ret)


if __name__ == '__main__':
    main()