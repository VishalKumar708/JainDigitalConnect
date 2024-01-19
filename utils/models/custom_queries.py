from django.db.models import F, Value, CharField, ExpressionWrapper, Case, When, IntegerField
from django.db.models.functions import Concat
from django.utils import timezone
from django.db import models


def calculate_age_expression(date_column, model):
    try:
        field = model._meta.get_field(date_column)
    except model._meta.get_field(date_column).DoesNotExist:
        raise ValueError(f"'{date_column}' is not a valid field in your model.")
    # Check if the field is of type DateField or DateTimeField
    if not isinstance(field, (models.DateField, models.DateTimeField)):
        raise ValueError(f"'{date_column}' should be a DateField or DateTimeField.")

    current_year = timezone.now().year

    age_expression = Case(
        When(
            dob__isnull=False,  # Check for 'dob' not being null
            then=ExpressionWrapper(
                Concat(
                    current_year - F(f'{date_column}__year') -
                    Case(
                        When(
                            **{f'{date_column}__month__gt': timezone.now().month},
                            then=1
                        ),
                        When(
                            **{f'{date_column}__month': timezone.now().month, f'{date_column}__day__gt': timezone.now().day},
                            then=1
                        ),
                        default=0,
                        output_field=IntegerField()
                    ),
                    Value(' Years'),
                    output_field=CharField()
                ),
                output_field=CharField()
            )
        ),
        default=Value(''),  # Return empty string if 'dob' is null
        output_field=CharField()
    )
    # print('query==> ', age_expression)
    return age_expression

