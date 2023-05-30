from django.db import models
from django.contrib.auth.models import User


# des qu'un user rentre quelque chose on récupère ces données

class CompileWorkflow(models.Model):
    created = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
