
from django.urls import path
from .state_views import CreateNewState, UpdateStateById, GetAllApprovedState, GetAllUnapprovedState, GetCitiesByStateId
from .city_views import CreateNewCity, UpdateCityById, GetCityById, GetAllApprovedCity, GetAllUnapprovedCity, GetAreaByCityId, GetAllBusinessByCityId
urlpatterns = [
    path('POSTNewState/', CreateNewState.as_view()),
    path('PUTStateById/<slug:stateId>/', UpdateStateById.as_view()),
    path('GETAllApprovedStates/', GetAllApprovedState.as_view()),
    path('GETAllUnapprovedStates/', GetAllUnapprovedState.as_view()),
    path('GETAllCitiesByStateId/<slug:stateId>/', GetCitiesByStateId.as_view()),

    #     City Apis
    path('POSTNewCity/', CreateNewCity.as_view()),
    path('PUTCityById/<slug:cityId>/', UpdateCityById.as_view()),
    path('GETCityByCityId/<slug:cityId>/', GetCityById.as_view()),
    path('GETAllUnapprovedCity/', GetAllUnapprovedCity.as_view()),
    path('GETAllApprovedCity/', GetAllApprovedCity.as_view()),
    path('GETAllAreasByCityId/<slug:cityId>/', GetAreaByCityId.as_view()),
    path('GETAllBusinessByCityId/<slug:cityId>/', GetAllBusinessByCityId.as_view()),

]
