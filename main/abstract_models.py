from django.db import models


class ModelWithUser(models.Model):
    class Meta:
        abstract = True

    def get_user(self):
        raise NotImplementedError
