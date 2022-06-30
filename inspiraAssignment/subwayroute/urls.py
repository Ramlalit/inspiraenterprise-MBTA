from django.urls import path
from subwayroute.views import LightAndHeavyRailList, MostAndFewest, ToAndFromStops

urlpatterns = [
    path('route/', LightAndHeavyRailList.as_view()),
    path('stops/', MostAndFewest.as_view()),
    path('source-to-destination/', ToAndFromStops.as_view()),

]