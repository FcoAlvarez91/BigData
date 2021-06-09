from django.db import models

# Create your models here.

class Query:
    custom: str
    city: str
    where: str
    limit: int
    min:int
    max:int
    