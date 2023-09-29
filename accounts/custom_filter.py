from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.response import Response

from django.http import JsonResponse
from .models import User
from .serializers import GETAllUserSerializer


def filter_queryset(request):
    # Get query parameters for filtering
    try:
        # Define your custom filtering logic based on query parameters
        name = request.GET.get('name')
        father_name = request.GET.get('fatherName')
        phone_number = request.GET.get('phoneNumber')
        native_place = request.GET.get('nativePlace')
        marital_status = request.GET.get('maritalStatus')
        profession = request.GET.get('profession')
        gender = request.GET.get('gender')
        gotra = request.GET.get('gotra')
        # age = request.GET.get('age')
        age_gt = request.GET.get('age__gte')
        age_lt = request.GET.get('age__lte')
        age_eq = request.GET.get('age__eq')
        # Initialize a Q object to construct the query
        query = Q()

        # Add case-insensitive matching for string fields
        if name:
            query |= Q(name__icontains=name)
        if father_name:
            query |= Q(fatherName__icontains=father_name)
        if phone_number:
            query |= Q(phoneNumber__icontains=phone_number)
        if native_place:
            query |= Q(nativePlace__icontains=native_place)
        if marital_status:
            query |= Q(maritalStatus__icontains=marital_status)
        if profession:
            query |= Q(profession__icontains=profession)
        if gender:
            query |= Q(gender__icontains=gender)
        if gotra:
            query |= Q(gotra__icontains=gotra)



        if age_gt:
            age_gt = int(age_gt)
            birthdate_upper = datetime.now().date() - timedelta(days=365 * age_gt)
            print('birth_upper ==> ', birthdate_upper)
            query &= Q(dob__lte=birthdate_upper)
            # queryset = User.objects.filter(dob__lte=birthdate_upper)

        if age_lt:
            age_lt = int(age_lt)
            birthdate_lower = datetime.now().date() - timedelta(days=365 * age_lt)
            # queryset = queryset.filter(dob__gt=birthdate_lower)
            query &= Q(dob__gte=birthdate_lower)
        #
        if age_eq:
            age_eq = int(age_eq)
            birthdate_exact = datetime.now().date() - timedelta(days=365 * age_eq)
            query &= Q(dob=birthdate_exact)
            # queryset = queryset.filter(dob=birthdate_exact)
        # Apply the constructed query to the queryset
        if query:
            queryset = User.objects.filter(query)
            print("your mysql query to filter data ==>", queryset.query)
            serializer = GETAllUserSerializer(queryset, many=True)
            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return JsonResponse(response_data)
        else:
            queryset = User.objects.all().order_by('name')
            serializer = GETAllUserSerializer(queryset, many=True)

            response_data = {
                'statusCode': 200,
                'status': 'success',
                'data': serializer.data
            }
            return JsonResponse(response_data, status=200)
    except Exception as e:
        response_data = {
            'statusCode': 500,
            'status': 'failed',
            'data': {'message': str(e)}
        }
        return JsonResponse(response_data, status=500)