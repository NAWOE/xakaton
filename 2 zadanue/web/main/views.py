from django.shortcuts import render
from .logic import solve_route
import math

# База данных достопримечательностей Вологды (настоящие координаты)
PLACES = [
    {'id': 0, 'name': 'Вологодский Кремль', 'lat': 59.223582, 'lon': 39.882379},
    {'id': 1, 'name': 'Памятник Батюшкову', 'lat': 59.224711, 'lon': 39.883986},
    {'id': 2, 'name': 'Памятник букве О', 'lat': 59.225055, 'lon': 39.882223},
    {'id': 3, 'name': 'Софийский собор', 'lat': 59.2245, 'lon': 39.8828},
    {'id': 4, 'name': 'Дом Петра I', 'lat': 59.209939, 'lon': 39.908146},
    {'id': 5, 'name': 'Музей кружева', 'lat': 59.223886, 'lon': 39.884770},
]


# Функция для расчета расстояния в метрах между двумя координатами
def get_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000  # Радиус Земли в метрах
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return int(R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def index(request):
    result_route = []
    total_dist = 0
    selected_ids = []
    max_d = 2000  # Значение по умолчанию

    if request.method == 'POST':
        # 1. Получаем данные из формы
        max_d = int(request.POST.get('distance', 1000))
        # Получаем список ID, которые отметил пользователь
        selected_str_ids = request.POST.getlist('places')
        selected_ids = [int(i) for i in selected_str_ids]

        # Если выбрали хотя бы 2 места
        if len(selected_ids) > 1:
            # 2. Строим под-список выбранных мест
            active_places = [p for p in PLACES if p['id'] in selected_ids]

            # 3. Генерируем матрицу расстояний для твоего алгоритма
            n = len(active_places)
            matrix = [[0] * n for _ in range(n)]

            for i in range(n):
                for j in range(n):
                    if i != j:
                        dist = get_distance_meters(
                            active_places[i]['lat'], active_places[i]['lon'],
                            active_places[j]['lat'], active_places[j]['lon']
                        )
                        matrix[i][j] = dist

            # 4. ЗАПУСКАЕМ ТВОЙ АЛГОРИТМ
            # Алгоритм вернет индексы внутри active_places (0..N-1)
            path_indices = solve_route(n, max_d, matrix)

            # 5. Превращаем индексы обратно в объекты достопримечательностей
            for idx in path_indices:
                result_route.append(active_places[idx])

    context = {
        'places': PLACES,
        'route': result_route,
        'selected_ids': selected_ids,
        'max_d': max_d
    }
    return render(request, 'main/index.html', context)