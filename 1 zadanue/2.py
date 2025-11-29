import sys
import time
import random


def solve():

    start_time = time.time()
    TIME_LIMIT = 0.95


    input_data = sys.stdin.read().split()
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


    sorted_neighbors = []
    for r in range(N):
        neighbors = []
        for c in range(N):
            if r != c:
                neighbors.append((dist_matrix[r][c], c))
        neighbors.sort(key=lambda x: x[0])
        sorted_neighbors.append(neighbors)


    best_path = []
    best_path_len = 0
    best_dist = float('inf')


    def update_best(path, dist):
        nonlocal best_path, best_path_len, best_dist
        count = len(path)

        if count > best_path_len:
            best_path = list(path)
            best_path_len = count
            best_dist = dist

        elif count == best_path_len:
            if dist < best_dist:
                best_path = list(path)
                best_dist = dist


    for start_node in range(N):
        current_path = [start_node]
        current_dist = 0
        visited = [False] * N
        visited[start_node] = True

        curr = start_node
        while True:
            moved = False

            for dist, neighbor in sorted_neighbors[curr]:
                if not visited[neighbor]:
                    if current_dist + dist <= D:
                        visited[neighbor] = True
                        current_path.append(neighbor)
                        current_dist += dist
                        curr = neighbor
                        moved = True
                        break

            if not moved:
                break

        update_best(current_path, current_dist)



    while time.time() - start_time < TIME_LIMIT:

        start_node = random.randint(0, N - 1)

        current_path = [start_node]
        current_dist = 0
        visited = [False] * N
        visited[start_node] = True

        curr = start_node
        while True:
            candidates = []

            limit_check = 0
            for dist, neighbor in sorted_neighbors[curr]:
                if not visited[neighbor] and current_dist + dist <= D:
                    candidates.append((dist, neighbor))
                    limit_check += 1
                    if limit_check >= 3:
                        break

            if not candidates:
                break


            chosen_dist, chosen_node = random.choice(candidates)

            visited[chosen_node] = True
            current_path.append(chosen_node)
            current_dist += chosen_dist
            curr = chosen_node

        update_best(current_path, current_dist)


    result_path = [x + 1 for x in best_path]
    print(len(result_path))
    print(*(result_path))


if __name__ == '__main__':
    solve()