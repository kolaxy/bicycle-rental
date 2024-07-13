from django.db import models


class BaseModel(models.Model):
    added_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ('-added_at',)

    @property
    def created(self):
        return f'{self.added_at.strftime("%X")} {self.added_at.strftime("%x")}'

    @property
    def updated(self):
        return f'{self.updated_at.strftime("%X")} {self.updated_at.strftime("%x")}'
