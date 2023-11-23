
from django.urls import path
from .state_views import POSTNewState, UpdateStateById, GetAllApprovedState, GetAllUnapprovedState, GetCitiesByStateId
from .city_views import POSTNewCity, UpdateCityById, GetCityDetailsById, GetAllApprovedCityAndSearchCityName, GetAllApprovedAndUnapprovedCityForAdmin, GetAllApprovedCityAndSearchCityNameForBusiness
from .area_views import POSTNewArea, UpdateAreaById, GetAllApprovedAreasByCityId, GetAllApprovedAndUnapprovedAreasForAdmin, GetAreaDetailsById, GETAllResidentsByAreaId
from .business_views import CreateNewBusiness, UpdateBusinessById, GetAllUnapprovedBusiness, GetBusinessById, GetAllApprovedBusinessByCityId
from .literature_views import CreateNewLiterature, UPDATELiterature, GetLiteratureById, GetAllApprovedLiterature, GetAllUnapprovedLiterature
from .mst_sect_view import POSTSect, PUTSectById, GETAllSectForDropDown, GETSectDetailById, GETAllSect,  GETAllSectSaint
from .saint_views import POSTNewSaint, PUTSaintById, GETAllSaintsBySearchParam, GETSaintDetailById, GETAllActiveSaintBySectIdUsingSearchParam, GETAllAddAndApprovedSaint
from .mst_blood_group_views import POSTNewBloodGroup, PUTBloodGroupById, GETBloodGroupDetailById, GETAllBloodGroup, GETAllBloodGroupForDropDown
from .mst_marital_status import POSTMaritalStatus, PUTMaritalStatusById, GETMaritalStatusDetailById, GETAllMaritalStatus, GETAllMaritalStatusForDropDown
from .mst_relation_views import POSTRelation, PUTRelationById, GETRelationDetailById, GETAllRelation, GETAllRelationForDropDown
from .mst_profession_views import POSTProfession, PUTProfessionById, GETProfessionDetailById, GETAllProfession, GETAllProfessionForDropDown


urlpatterns = [
    path('POSTNewState/', POSTNewState.as_view()),  # correct
    path('PUTStateById/<slug:stateId>/', UpdateStateById.as_view()),  # correct
    path('GETAllApprovedStates/', GetAllApprovedState.as_view()),  # correct
    path('GETAllUnapprovedStates/', GetAllUnapprovedState.as_view()),  # correct
    path('GETAllCitiesByStateId/<slug:stateId>/', GetCitiesByStateId.as_view()),  # correct

    #     City Apis
    path('POSTNewCity/', POSTNewCity.as_view()),  # correct
    path('PUTCityById/<slug:cityId>/', UpdateCityById.as_view()),  # correct
    path('GetCityDetailsById/<slug:cityId>/', GetCityDetailsById.as_view()),  # correct
    path('GetAllApprovedAndUnapprovedCityForAdmin/', GetAllApprovedAndUnapprovedCityForAdmin.as_view()),  # correct
    path('GetAllApprovedCityAndSearchCityName/', GetAllApprovedCityAndSearchCityName.as_view()),  # correct
    path('GetCityByBusiness/', GetAllApprovedCityAndSearchCityNameForBusiness.as_view()),  # new add

    #     Area Apis
    path('POSTNewArea/', POSTNewArea.as_view()),  # correct
    path('PUTAreaById/<slug:areaId>/', UpdateAreaById.as_view()),  # correct
    path('GETAllApprovedAreasByCityId/<slug:cityId>/', GetAllApprovedAreasByCityId.as_view()),  # correct
    path('GETAllApprovedAndUnapprovedAreasForAdmin/', GetAllApprovedAndUnapprovedAreasForAdmin.as_view()),  # correct
    path('GETAreaDetailsById/<slug:areaId>/', GetAreaDetailsById.as_view()),  # correct
    path('GETAllResidentsByAreaId/<slug:areaId>/', GETAllResidentsByAreaId.as_view()),  # new




    #     Business Api
    path('POSTNewBusiness/', CreateNewBusiness.as_view()),
    path('PUTBusinessById/<slug:businessId>/', UpdateBusinessById.as_view()),
    path('GETAllApprovedBusinessByCityId/<slug:cityId>/', GetAllApprovedBusinessByCityId.as_view()),  # correct
    path('GETAllUnapprovedBusiness/', GetAllUnapprovedBusiness.as_view()),
    path('GETBusinessById/<slug:businessId>/', GetBusinessById.as_view()),

    #     Literature Api
    path('POSTNewLiterature/', CreateNewLiterature.as_view()),
    path('PUTLiteratureById/<slug:literatureId>/', UPDATELiterature.as_view()),
    path('GETAllApprovedLiterature/', GetAllApprovedLiterature.as_view()),
    path('GETAllUnapprovedLiterature/', GetAllUnapprovedLiterature.as_view()),
    path('GETLiteratureById/<slug:literatureId>/', GetLiteratureById.as_view()),


    #  count for saint
    path('GETAllSectSaint/', GETAllSectSaint.as_view()),

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
    path('GETAllAddAndApprovedSaint/', GETAllAddAndApprovedSaint.as_view()),

    #     Sect
    path('POSTSect/', POSTSect.as_view()),
    path('PUTSectById/<slug:id>/', PUTSectById.as_view()),
    path('GETSectDetailById/<slug:id>/', GETSectDetailById.as_view()),
    path('GETAllSect/', GETAllSect.as_view()),
    path('GETAllSectForDropDown/', GETAllSectForDropDown.as_view()),

    # Blood Group
    path('POSTNewBloodGroup/', POSTNewBloodGroup.as_view()),
    path('PUTBloodGroupById/<slug:id>/', PUTBloodGroupById.as_view()),
    path('GETBloodGroupDetailById/<slug:id>/', GETBloodGroupDetailById.as_view()),
    path('GETAllBloodGroups/', GETAllBloodGroup.as_view()),
    path('GETAllBloodGroupForDropDown/', GETAllBloodGroupForDropDown.as_view()),

    # MaritalStatus
    path('POSTMaritalStatus/', POSTMaritalStatus.as_view()),
    path('PUTMaritalStatusById/<slug:id>/', PUTMaritalStatusById.as_view()),
    path('GETMaritalStatusDetailById/<slug:id>/', GETMaritalStatusDetailById.as_view()),
    path('GETAllMaritalStatus/', GETAllMaritalStatus.as_view()),
    path('GETAllMaritalStatusForDropDown/', GETAllMaritalStatusForDropDown.as_view()),

    # Relation
    path('POSTRelation/', POSTRelation.as_view()),
    path('PUTRelationById/<slug:id>/', PUTRelationById.as_view()),
    path('GETRelationDetailsById/<slug:id>/', GETRelationDetailById.as_view()),
    path('GETAllRelation/', GETAllRelation.as_view()),
    path('GETAllRelationForDropDown/', GETAllRelationForDropDown.as_view()),

    # Profession
    path('POSTProfession/', POSTProfession.as_view()),
    path('PUTProfessionById/<slug:id>/', PUTProfessionById.as_view()),
    path('GETProfessionDetailsById/<slug:id>/', GETProfessionDetailById.as_view()),
    path('GETAllProfession/', GETAllProfession.as_view()),
    path('GETAllProfessionForDropDown/', GETAllProfessionForDropDown.as_view()),

]

