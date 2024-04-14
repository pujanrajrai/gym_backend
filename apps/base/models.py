from django.db import models
from uuid import uuid4


class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    objects = NonDeleted()

    everything = models.Manager()

    class Meta:
        ordering = ['-created_date']
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
