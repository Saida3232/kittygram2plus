from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
#from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    #throttle_classes = (WorkingHoursRateThrottle)
    # А далее применится лимит low_request
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    pagination_class = None
    filterset_fields = ('color','birth_year')
    search_fields = ('name',)
    ordering_fields = ('=name','birth_year',)
    ordering = ('birth_year')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Cat.objects.all()
        color = self.request.query_params.get('color')
        if color is not None:

            queryset = queryset.filter(color=color)
        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
