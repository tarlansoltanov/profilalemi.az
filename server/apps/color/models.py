from django.db import models


class Color(models.Model):
    """Model definition for Color."""

    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Color."""

        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        """Unicode representation of Color."""
        return self.name