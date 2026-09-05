from django.urls import path
from .views import HomeSwiperView, HomeIntroView, HomeStatsView

urlpatterns = [
    path("swiper/", HomeSwiperView.as_view()),
    path("intro/", HomeIntroView.as_view()),
    path("stats/", HomeStatsView.as_view()),
]
