
from django.urls import path

from .emergency.views import *
from .business.views import *
from .state.views import *
from .city.views import *
from .area.views import *
from .saint.views import *
from .literature.views import *
from .aarti.views import *
from .dharam_sthan.views import *
from .dharam_sthan.dharamSthanMember_views import *
from .dharam_sthan.dharamSthanHistory_views import *
from .events.views import *
from .resident.views import *

from .master_views.maritalStatus_views import *
from .master_views.sect_views import *
from .master_views.bloodGroup_views import *
from .master_views.profession_views import *
from .master_views.relation_views import *
from .live_location.views import *

urlpatterns = [
    #  state  ---correct
    path('POSTNewState/', POSTNewState.as_view()),  # correct
    path('PUTStateById/<slug:stateId>/', UpdateStateById.as_view()),  # correct
    path('GETStateDetailsById/<slug:stateId>/', GETStateDetailsById.as_view()),
    path('GETAllApprovedStates/', GetAllApprovedState.as_view()),  # correct
    path('GETAllUnapprovedStates/', GetAllUnapprovedState.as_view()),  # correct
    path('GETAllCitiesByStateId/<slug:stateId>/', GetCitiesByStateId.as_view()),  # correct

    #     City Apis  ---correct
    path('POSTNewCity/', POSTNewCity.as_view()),  # correct
    path('PUTCityById/<slug:cityId>/', UpdateCityById.as_view()),  # correct
    path('GetCityDetailsById/<slug:cityId>/', GetCityDetailsById.as_view()),  # correct
    path('GetAllApprovedAndUnapprovedCityForAdmin/', GetAllApprovedAndUnapprovedCityForAdmin.as_view()),  # correct



    #     Area Apis  ---correct
    path('POSTNewArea/', POSTNewArea.as_view()),  # correct
    path('PUTAreaById/<slug:areaId>/', UpdateAreaById.as_view()),  # correct
    path('GETAllApprovedAndUnapprovedAreasForAdmin/', GetAllApprovedAndUnapprovedAreasForAdmin.as_view()),  # correct
    path('GETAreaDetailsById/<slug:areaId>/', GetAreaDetailsById.as_view()),  # correct



    #     Business Api  ---correct
    path('POSTNewBusinessBy/', POSTNewBusiness.as_view()),
    path('PUTBusinessById/<slug:businessId>/', PUTBusinessById.as_view()),
    path('GETAllApprovedBusinessByCityId/<slug:cityId>/', GetAllApprovedBusinessByCityId.as_view()),  # correct
    path('GetAllApprovedAndUnapprovedBusiness/', GetAllApprovedAndUnapprovedBusiness.as_view()),
    path('GETBusinessDetailsById/<slug:businessId>/', GetBusinessDetailsById.as_view()),
    path('GETAllBusinessByUserId/<slug:userId>/', GETAllBusinessByUserId.as_view()),
    path('GetCityByBusiness/', GetAllApprovedCityAndSearchCityNameForBusiness.as_view()),  # new add

    #     Literature Api
    path('GETAllSectLiterature/',GETAllSectLiterature.as_view()),  # correct
    path('POSTNewLiterature/', POSTNewLiterature.as_view()),  # correct
    path('PUTLiteratureById/<slug:literatureId>/', UPDATELiterature.as_view()),
    path('GETAllApprovedLiteratureBySectId/<slug:sectId>/', GETAllApprovedLiteratureBySectId.as_view()),
    path('GETAllApprovedAndUnapprovedLiterature/', GETAllApprovedAndUnapprovedLiterature.as_view()),  # correct
    path('GETLiteratureById/<slug:literatureId>/', GETLiteratureById.as_view()),


    # count for residents
    # path('GETAllSectResident/', GETAllSectResidents.as_view()),

    #     Saint  ---correct
    #  count for saint
    path('GETAllSectSaint/', GETAllSectSaint.as_view()),
    # create new saint
    path('POSTNewSaint/', POSTNewSaint.as_view()),
    # update saint
    path('PUTSaintById/<slug:id>/', PUTSaintById.as_view()),
    # for search only Saints, for end user use 'saintName' param
    path('GETAllSaintsBySectIdUsingSearchParam/<slug:sectId>/', GETAllSaintsBySearchParam.as_view()),
    # it takes saint id and return all details
    path('GETSaintDetailById/<slug:saintId>/', GETSaintDetailById.as_view()),
    # it takes sectId and 'gender' param
    path('GETAllActiveSaintBySectId/<slug:sectId>/', GETAllActiveSaintBySectId.as_view()),
    #  for admin, it takes one parameter 'status'
    path('GETAllAddAndApprovedSaint/', GETAllAddAndApprovedSaint.as_view()),


    #     Sect
    path('POSTSect/', POSTSect.as_view()),
    path('PUTSectById/<slug:id>/', PUTSectById.as_view()),
    path('GETSectDetailById/<slug:id>/', GETSectDetailById.as_view()),
    path('GETAllSectForAdmin/', GETAllSectForAdmin.as_view()),
    path('GETAllSectForDropDown/', GETAllSectForDropDown.as_view()),

    # Blood Group
    path('POSTNewBloodGroup/', POSTNewBloodGroup.as_view()),
    path('PUTBloodGroupById/<slug:id>/', PUTBloodGroupById.as_view()),
    path('GETBloodGroupDetailById/<slug:id>/', GETBloodGroupDetailById.as_view()),
    path('GETAllBloodGroupsForAdmin/', GETAllBloodGroupForAdmin.as_view()),
    path('GETAllBloodGroupForDropDown/', GETAllBloodGroupForDropDown.as_view()),

    # MaritalStatus
    path('POSTMaritalStatus/', POSTMaritalStatus.as_view()),
    path('PUTMaritalStatusById/<slug:id>/', PUTMaritalStatusById.as_view()),
    path('GETMaritalStatusDetailById/<slug:id>/', GETMaritalStatusDetailById.as_view()),
    path('GETAllMaritalStatusForAdmin/', GETAllMaritalStatusForAdmin.as_view()),
    path('GETAllMaritalStatusForDropDown/', GETAllMaritalStatusForDropDown.as_view()),

    # Relation
    path('POSTRelation/', POSTRelation.as_view()),
    path('PUTRelationById/<slug:id>/', PUTRelationById.as_view()),
    path('GETRelationDetailsById/<slug:id>/', GETRelationDetailById.as_view()),
    path('GETAllRelationForAdmin/', GETAllRelationForAdmin.as_view()),
    path('GETAllRelationForDropDown/', GETAllRelationForDropDown.as_view()),

    # Profession
    path('POSTProfession/', POSTProfession.as_view()),
    path('PUTProfessionById/<slug:id>/', PUTProfessionById.as_view()),
    path('GETProfessionDetailsById/<slug:id>/', GETProfessionDetailById.as_view()),
    path('GETAllProfessionForAdmin/', GETAllProfessionForAdmin.as_view()),
    path('GETAllProfessionForDropDown/', GETAllProfessionForDropDown.as_view()),

    # Emergency  ---correct
    path('GETAllCityByEmergency/', GETAllCityByEmergency.as_view()),
    path('POSTEmergency/', POSTEmergency.as_view()),
    path('PUTEmergencyById/<slug:id>/', PUTEmergencyById.as_view()),
    path('GETEmergencyDetailsById/<slug:id>/', GETEmergencyDetailById.as_view()),
    path('GETAllEmergencyByCityId/<slug:cityId>/', GETAllEmergencyByCityId.as_view()),
    path('GETAllEmergencyForAdmin/', GETAllEmergencyForAdmin.as_view()),

    # Aarti
    path('GETAllSectByAarti/', GETAllSectAarti.as_view()),
    path('POSTNewAarti/', POSTNewAarti.as_view()),
    path('PUTAartiById/<slug:aartiId>/', UPDATEAarti.as_view()),
    path('GETAartiDetailsById/<slug:aartiId>/', GETAartiDetailsById.as_view()),
    path('GETAllApprovedAartiBySectId/<slug:sectId>/', GETAllApprovedAartiBySectId.as_view()),
    path('GETAllApprovedAndUnapprovedLiteratureForAdmin/', GETAllApprovedAndUnapprovedLiteratureForAdmin.as_view()),

    # Dharam Sthan
    path('POSTNewDharamSthan/', POSTNewDharamSthan.as_view()),
    path('PUTDharamSthanById/<slug:dharamSthanId>/', PUTDharamSthanById.as_view()),
    path('GETAllCityBySectIdDharamSthan/<slug:sectId>/', GETAllCityBySectIdDharamSthan.as_view()),
    path('GETAllApprovedDharamSthanBySectIdAndCityId/<slug:sectId>/<slug:cityId>/', GETAllApprovedDharamSthanBySectId.as_view()),
    path('GETDharamSthanDetailsById/<slug:dharamSthanId>/', GETDharamSthanDetailsById.as_view()),
    # for admin
    path('GETAllApprovedAndUnapprovedDharamSthanByCityIdForAdmin/<slug:cityId>/', GETAllApprovedAndUnapprovedDharamSthanByCityIdForAdmin.as_view()),
    path('GETAllCityDharamSthanForAdmin/', GETAllCityDharamSthanForAdmin.as_view()),

    # Dharam Sthan Member
    path('POSTNewDharamSthanMember/', POSTNewDharamSthanMember.as_view()),
    path('PUTDharamSthanMemberById/<slug:dharamSthanMemberId>/', PUTDharamSthanMemberById.as_view()),
    path('GETDharamSthanMemberDetailsById/<slug:dharamSthanMemberId>/', GETDharamSthanMemberDetailsById.as_view()),
    path('GETAllDharamSthanMembersByDharamSthanId/<slug:dharamSthanId>/', GETAllDharamSthanMembersByDharamSthanId.as_view()),

    # Dharam Sthan History
    path('POSTNewDharamSthanHistory/', POSTNewDharamSthanHistory.as_view()),
    path('PUTDharamSthanHistoryById/<slug:dharamSthanHistoryId>/', PUTDharamSthanHistoryById.as_view()),
    path('GETDharamSthanHistoryDetailsById/<slug:dharamSthanHistoryId>/', GETDharamSthanHistoryDetailsById.as_view()),
    path('GETAllActiveDharamSthanHistoryBydharamSthanId/<slug:dharamSthanId>/', GETAllActiveDharamSthanHistoryBydharamSthanId.as_view()),
    path('GETAllDharamSthanHistoryBydharamSthanIdForAdmin/<slug:dharamSthanId>/',GETAllDharamSthanHistoryBydharamSthanIdForAdmin.as_view()),

    # Events
    path('POSTNewEvent/', POSTNewEvent.as_view()),
    path('PUTEventById/<slug:eventId>/', PUTEventById.as_view()),
    path('GETEventDetailsById/<slug:eventId>/', GETEventDetailsById.as_view()),
    path('GETAllSectEvent/', GETAllSectEvent.as_view()),
    path('GETAllCityEventBySectId/<slug:sectId>/', GETAllCityEventBySectId.as_view()),
    path('GETAllActiveEventBySectIdAndCityId/<slug:sectId>/<slug:cityId>/', GETAllActiveEventBySectIdAndCityId.as_view()),
    path('GETAllApprovedAndUnapprovedEventForAdmin/', GETAllApprovedAndUnapprovedEventForAdmin.as_view()),

    #     Residents
    #  city wise
    path('GETAllApprovedCityAndSearchCityName/', GETAllApprovedCityAndSearchCityName.as_view()),  # correct
    path('GETAllApprovedAreasByCityId/<slug:cityId>/', GetAllApprovedAreasByCityId.as_view()),  # correct
    path('GETAllResidentsByAreaId/<slug:areaId>/', GETAllResidentsByAreaId.as_view()),  # new
    #  sect wise
    path('GETAllSectResident/', GETAllSectResident.as_view()),
    path('GETAllApprovedCityBySectId/<slug:sectId>/', GETAllApprovedCityBySectId.as_view()),
    path('GETAllApprovedAreasBySectIdAndCityId/<slug:sectId>/<slug:cityId>/', GETAllApprovedAreasBySectIdAndCityId.as_view()),
    path('GETAllResidentsBySectIdAndAreaId/<slug:sectId>/<slug:areaId>/', GETAllResidentsBySectIdAndAreaId.as_view()),

    # Live Location
    path('POSTNewLiveLocation/', POSTNewLiveLocation.as_view()),
    path('PUTLiveLocationById/<slug:liveLocationId>/', PUTLiveLocationById.as_view()),
    path('GETLiveLocationDetailsById/<slug:liveLocationId>/', GETLiveLocationDetailsById.as_view()),
    path('GETAllLiveLocationByUserId/<slug:userId>/', GETAllLiveLocationByUserId.as_view()),
    #  if live location is off
    path('GETAllSectDharamSthanHistory/', GETAllSectDharamSthanHistory.as_view()),
    path('GETAllDharamSthanHistoryBySectId/<slug:sectId>/', GETAllDharamSthanHistoryBySectId.as_view()),
    path('GETDharamSthanDetailsByDharamSthanIdForLiveLocation/<slug:dharamSthanId>/', GETDharamSthanDetailsByDharamSthanIdForLiveLocation.as_view()),

]

