
from django.urls import path
from .state_views import CreateNewState, UpdateStateById, GetAllApprovedState, GetAllUnapprovedState, GetCitiesByStateId
from .city_views import CreateNewCity, UpdateCityById, GetCityById, GetAllApprovedCity, GetAllUnapprovedCity, GetAreaByCityId, GetAllBusinessByCityId
from .area_views import CreateNewArea, UpdateAreaById, GetAllApprovedAreas, GetAllUnapprovedAreas, GetAreaById
from .business_views import CreateNewBusiness, UpdateBusinessById, GetAllUnapprovedBusiness, GetBusinessById, GetAllApprovedBusiness
from .literature_views import CreateNewLiterature, UPDATELiterature, GetLiteratureById, GetAllApprovedLiterature, GetAllUnapprovedLiterature
from .sect_view import GETAllSect, GETAllSectWithCount
from .saint_views import POSTNewSaint, PUTSaintById, GETAllSaintsBySearchParam, GETSaintDetailById, GETAllActiveSaintBySectIdUsingSearchParam, GETAllAddAndApprovedSaint
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
    path('GETAllApprovedBusiness/', GetAllApprovedBusiness.as_view()),
    path('GETAllUnapprovedBusiness/', GetAllUnapprovedBusiness.as_view()),
    path('GETBusinessById/<slug:businessId>/', GetBusinessById.as_view()),

    #     Literature Api
    path('POSTNewLiterature/', CreateNewLiterature.as_view()),
    path('PUTLiteratureById/<slug:literatureId>/', UPDATELiterature.as_view()),
    path('GETAllApprovedLiterature/', GetAllApprovedLiterature.as_view()),
    path('GETAllUnapprovedLiterature/', GetAllUnapprovedLiterature.as_view()),
    path('GETLiteratureById/<slug:literatureId>/', GetLiteratureById.as_view()),

    #     Sect
    path('GETAllSect/', GETAllSect.as_view()),
    #  for saint
    path('GETAllSectWithCount/', GETAllSectWithCount.as_view()),

    #     Saint
    # create new saint
    path('POSTNewSaint/', POSTNewSaint.as_view()),
    # update saint
    path('PUTSaintById/<slug:id>/', PUTSaintById.as_view()),
    # for search Saints, for end user use 'search' param
    path('GETAllSaintsBySectIdUsingSearchParam/<slug:sectId>/', GETAllSaintsBySearchParam.as_view()),
    # it takes saint id and return all details
    path('GETSaintDetailById/<slug:saintId>/', GETSaintDetailById.as_view()),
    # it takes sectId and 'gender' param
    path('GETAllActiveSaintBySectId/<slug:sectId>/', GETAllActiveSaintBySectIdUsingSearchParam.as_view()),
    #  for admin, it takes one parameter 'status'
    path('GETAllAddAndApprovedSaint/', GETAllAddAndApprovedSaint.as_view())
]

