from django.urls import path
from subwayroute.views import LightAndHeavyRailList, MostAndFewest

urlpatterns = [
    path('route/', LightAndHeavyRailList.as_view()),
    path('stops/', MostAndFewest.as_view()),

]