# main/logic.py
import time
import random


def solve_route(n, d, dist_matrix):
    """
    n: количество выбранных точек
    d: лимит расстояния (в метрах)
    dist_matrix: матрица расстояний между выбранными точками
    Возвращает: список индексов лучших точек
    """

    start_time = time.time()
    TIME_LIMIT = 0.95

    # ТВОЙ АЛГОРИТМ НАЧИНАЕТСЯ ЗДЕСЬ
    # (Я убрал чтение sys.stdin, так как данные приходят аргументами)

    # Предподсчет соседей
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

    # 1. Жадный проход
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

    # 2. Рандомный проход (пока есть время)
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

    return best_path  # Возвращаем список индексов (например [0, 2, 5])