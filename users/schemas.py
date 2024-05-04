from ninja import ModelSchema, Schema
from django.contrib.auth.models import User


class UserFullSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["password", "groups"]
