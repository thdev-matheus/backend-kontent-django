from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=50, null=False)
    module = models.TextField(null=False)
    students = models.IntegerField(null=False)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"<[{self.id}] {self.title} - {self.module}>"
