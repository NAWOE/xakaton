from django.db import models


class UserRoute(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название маршрута")
    description = models.TextField(blank=True, verbose_name="Описание")
    max_distance = models.IntegerField(verbose_name="Максимальное расстояние")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name


class RoutePoint(models.Model):
    route = models.ForeignKey(UserRoute, on_delete=models.CASCADE, related_name='points')
    place_id = models.IntegerField(verbose_name="ID достопримечательности")
    place_name = models.CharField(max_length=200, verbose_name="Название места")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    order = models.IntegerField(verbose_name="Порядок в маршруте")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.place_name}"