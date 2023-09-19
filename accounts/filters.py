
from django.db.models import Q


def filter_queryset(query_params=None, page_query_param = 'page'):
    filters = {}
    for param_name, param_value in query_params.items():
        # Create a case-insensitive search for string fields
        if param_name != page_query_param:
            filters[f"{param_name.strip()}__icontains"] = param_value.strip()
    # print("Your filter parameters ==> ", filters)
    # Apply filters to the queryset using Q objects
    q_objects = Q()
    for field, value in filters.items():
        q_objects |= Q(**{field: value})
    # print('query objects', q_objects)
    return q_objects

    # try:
    #     queryset = CustomUser.objects.filter(q_objects)
    #     print("This is your query==> ", queryset.query)
    #     return True
    # except Exception as e:
    #     # if not queryset.exists():
    #         # response_data = {
    #         #     'statusCode': 404,
    #         #     'status': 'failed',
    #         #     'data': {'msg': f'User Not found.{e}'},
    #         # }
    #         # return Response(response_data)
    #     return False
