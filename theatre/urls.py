from django.urls import path, include
from rest_framework import routers
from .views import (
    TheatreHallViewSet,
    GenreViewSet,
    ActorViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register(r"theatrehalls", TheatreHallViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"plays", PlayViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "theatre"
