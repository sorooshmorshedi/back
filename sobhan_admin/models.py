from django.db import models

from helpers.models import BaseModel, DATE, EXPLANATION
from users.models import User


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True, related_name='profile')

    company_name = models.CharField(max_length=150)
    business_type = models.CharField(max_length=150)

    sale_date = DATE()
    selling_type = models.CharField(max_length=150)

    explanation = EXPLANATION()
