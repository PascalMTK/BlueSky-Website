from django.db import models


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    country = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
