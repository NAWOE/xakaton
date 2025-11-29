from django.shortcuts import render, redirect
from django.http import JsonResponse
from .logic import solve_route
import math

# База данных достопримечательностей Вологды (настоящие координаты)
PLACES = [
    {'id': 0, 'name': 'Вологодский Кремль', 'lat': 59.223676349077465, 'lon': 39.88208234310151},
    {'id': 1, 'name': 'Памятник Батюшкову', 'lat': 59.224711, 'lon': 39.883986},
    {'id': 2, 'name': 'Памятник букве О', 'lat': 59.22505152009995, 'lon': 39.882178902626045},
    {'id': 3, 'name': 'Софийский собор', 'lat': 59.224381783051925, 'lon': 39.882409572601325},
    {'id': 4, 'name': 'Дом Петра I', 'lat': 59.209939, 'lon': 39.908146},
    {'id': 5, 'name': 'Музей кружева', 'lat': 59.223819083976814, 'lon': 39.884764552116394},
    {'id': 6, 'name': 'Шаламовский дом', 'lat': 59.22505152009995, 'lon': 39.882178902626045},
    {'id': 7, 'name': 'Памятник Ивану Грозному', 'lat': 59.22340460213793, 'lon': 39.883686304092414},
    {'id': 8, 'name': 'Краеведческий музей заповедник', 'lat': 59.22358027717441, 'lon': 39.88159954547883},
    {'id': 9, 'name': 'Картинная галерея', 'lat': 59.22374222679751, 'lon': 39.883434176445014},
    {'id': 10, 'name': 'Храм покрова Богородицы на Торгу', 'lat': 59.2235061643787, 'lon': 39.88679766654969},
    {'id': 11, 'name': 'Церковь Казанской иконы Богоматери на Торгу', 'lat': 59.222594838324355, 'lon': 39.887205362319946},
    {'id': 12, 'name': 'Вологодское кружево', 'lat': 59.22218034161501, 'lon': 39.88427639007569},
    {'id': 13, 'name': 'Девочка с мороженым', 'lat': 59.22196073866909, 'lon': 39.884174466133125},
    {'id': 14, 'name': 'Часовня 2000-летия Рождества Христова', 'lat': 59.225150332649925, 'lon': 39.87987756729126},
    {'id': 15, 'name': 'Лиса и Колобок', 'lat': 59.225150332649925, 'lon': 39.87987756729126},
    {'id': 16, 'name': 'Ладья', 'lat': 59.22383829824457, 'lon': 39.87774252891541},
    {'id': 17, 'name': 'Памятник В.В. Маяковскому', 'lat': 59.22292149112416, 'lon': 39.87909972667695},
    {'id': 18, 'name': 'Квартира Батюшкова К.Н.', 'lat': 59.22146388178832, 'lon': 39.883412718772895}
]

def get_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000  # Радиус Земли в метраx
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

    # Пытаемся загрузить сохраненные маршруты
    try:
        from .models import UserRoute
        saved_routes = UserRoute.objects.all().order_by('-created_at')[:10]
    except Exception:
        # Если таблицы еще не созданы, используем пустой список
        saved_routes = []

    if request.method == 'POST':
        # Обработка построения маршрута
        if 'build_route' in request.POST:
            max_d = int(request.POST.get('distance', 1000))
            selected_str_ids = request.POST.getlist('places')
            selected_ids = [int(i) for i in selected_str_ids]

            if len(selected_ids) > 1:
                active_places = [p for p in PLACES if p['id'] in selected_ids]
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

                path_indices = solve_route(n, max_d, matrix)
                for idx in path_indices:
                    result_route.append(active_places[idx])

        # Обработка сохранения маршрута
        elif 'save_route' in request.POST:
            route_name = request.POST.get('route_name', '').strip()
            route_description = request.POST.get('route_description', '').strip()

            if route_name and result_route:
                try:
                    from .models import UserRoute, RoutePoint
                    # Сохраняем маршрут в БД
                    user_route = UserRoute.objects.create(
                        name=route_name,
                        description=route_description,
                        max_distance=max_d
                    )

                    # Сохраняем точки маршрута
                    for order, point in enumerate(result_route, 1):
                        RoutePoint.objects.create(
                            route=user_route,
                            place_id=point['id'],
                            place_name=point['name'],
                            lat=point['lat'],
                            lon=point['lon'],
                            order=order
                        )

                    # Обновляем список сохраненных маршрутов
                    saved_routes = UserRoute.objects.all().order_by('-created_at')[:10]

                    # Перенаправляем, чтобы избежать повторной отправки формы
                    return redirect('index')

                except Exception as e:
                    # Если ошибка при сохранении
                    print(f"Ошибка при сохранении маршрута: {e}")

    context = {
        'places': PLACES,
        'route': result_route,
        'selected_ids': selected_ids,
        'max_d': max_d,
        'saved_routes': saved_routes
    }
    return render(request, 'main/index.html', context)


def load_route(request, route_id):
    """Загрузка сохраненного маршрута"""
    try:
        from .models import UserRoute
        user_route = UserRoute.objects.get(id=route_id)
        route_points = user_route.points.all()

        route_data = {
            'name': user_route.name,
            'description': user_route.description,
            'max_distance': user_route.max_distance,
            'points': list(route_points.values('place_id', 'place_name', 'lat', 'lon', 'order'))
        }

        return JsonResponse(route_data)
    except Exception as e:
        return JsonResponse({'error': 'Маршрут не найден или база данных не доступна'}, status=404)


def delete_route(request, route_id):
    """Удаление маршрута"""
    if request.method == 'POST':
        try:
            from .models import UserRoute
            user_route = UserRoute.objects.get(id=route_id)
            user_route.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': 'Маршрут не найден'}, status=404)
    return JsonResponse({'error': 'Неверный метод'}, status=400)