from django.urls import path

from .marital_status.views import *
from .bloodgroup.views import *
from .feedback_title.views import *
from .profession.views import *
from .sect.views import *
from .relation.views import *

urlpatterns = [
    #  Sect
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

    # Feedback Title
    path('POSTNewFeedbackTitle/', POSTNewFeedbackTitle.as_view()),
    path('PUTFeedbackTitleById/<slug:id>/', PUTFeedbackTitleById.as_view()),
    path('GETFeedbackTitleDetailById/<slug:id>/', GETFeedbackTitleDetailById.as_view()),
    path('GETAllFeedbackTitleForAdmin/', GETAllFeedbackTitleForAdmin.as_view()),
    path('GETAllFeedbackTitleForDropDown/', GETAllFeedbackTitleForDropDown.as_view()),
]
