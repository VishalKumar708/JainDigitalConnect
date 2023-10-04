
from django.urls import path
from .state_views import CreateNewState, UpdateStateById, GetAllApprovedState, GetAllUnapprovedState, GetCitiesByStateId
from .city_views import CreateNewCity, UpdateCityById, GetCityById, GetAllApprovedCity, GetAllUnapprovedCity, GetAreaByCityId, GetAllBusinessByCityId
from .area_views import CreateNewArea, UpdateAreaById, GetAllApprovedAreas, GetAllUnapprovedAreas, GetAreaById
from .business_views import CreateNewBusiness, UpdateBusinessById
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

    #     Area Apis
    path('POSTNewArea/', CreateNewArea.as_view()),
    path('PUTAreaById/<slug:areaId>/', UpdateAreaById.as_view()),
    path('GETAllApprovedAreas/', GetAllApprovedAreas.as_view()),
    path('GETAllUnapprovedAreas/', GetAllUnapprovedAreas.as_view()),
    path('GETAreaById/<slug:areaId>/', GetAreaById.as_view()),

    #     Business Api
    path('POSTNewBusiness/', CreateNewBusiness.as_view()),
    path('PUTBusinessById/<slug:businessId>/', UpdateBusinessById.as_view()),






]
