import sys
sys.setrecursionlimit(3000)
def solve():
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return
    if not input_data: return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        D = int(next(iterator))
        dist_matrix = []
        for _ in range(N):
            dist_matrix.append([int(next(iterator)) for _ in range(N)])
    except StopIteration:
        return

    best_path = []
    best_dist = float('inf')
    visited = [False] * N

    def find_route(u, current_dist, count, path):
        nonlocal best_path, best_dist
        if count > len(best_path):
            best_path = list(path)
            best_dist = current_dist

        elif count == len(best_path):
            if current_dist < best_dist:
                best_path = list(path)
                best_dist = current_dist
        remaining_nodes = N - len(path)
        if count + remaining_nodes < len(best_path):
            return
        if count + remaining_nodes == len(best_path) and current_dist >= best_dist:
            return
        for v in range(N):
            if not visited[v]:
                d = dist_matrix[u][v]
                if current_dist + d <= D:
                    visited[v] = True
                    path.append(v)

                    find_route(v, current_dist + d, count + 1, path)

                    path.pop()
                    visited[v] = False

    for start_node in range(N):
        visited[start_node] = True
        find_route(start_node, 0, 1, [start_node])
        visited[start_node] = False

    result_path = [x + 1 for x in best_path]
    print(len(result_path))
    print(*(result_path))


if __name__ == '__main__':
    solve()