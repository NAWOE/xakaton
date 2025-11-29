import time
import random

def solve_route(n, d, dist_matrix):
    """
    n: int - количество точек
    d: int - лимит расстояния
    dist_matrix: list of lists - матрица расстояний
    Returns: list - список индексов маршрута (например [0, 2, 4])
    """
    start_time = time.time()
    TIME_LIMIT = 0.95

    # Предподсчет соседей (твоя логика)
    sorted_neighbors = []
    for r in range(n):
        neighbors = []
        for c in range(n):
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

    # Основной цикл (твоя логика)
    # 1. Жадный
    for start_node in range(n):
        current_path = [start_node]
        current_dist = 0
        visited = [False] * n
        visited[start_node] = True
        curr = start_node
        while True:
            moved = False
            for dist, neighbor in sorted_neighbors[curr]:
                if not visited[neighbor]:
                    if current_dist + dist <= d:
                        visited[neighbor] = True
                        current_path.append(neighbor)
                        current_dist += dist
                        curr = neighbor
                        moved = True
                        break
            if not moved:
                break
        update_best(current_path, current_dist)

    # 2. Рандом
    while time.time() - start_time < TIME_LIMIT:
        start_node = random.randint(0, n - 1)
        current_path = [start_node]
        current_dist = 0
        visited = [False] * n
        visited[start_node] = True
        curr = start_node
        while True:
            candidates = []
            limit_check = 0
            for dist, neighbor in sorted_neighbors[curr]:
                if not visited[neighbor] and current_dist + dist <= d:
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

    return best_path