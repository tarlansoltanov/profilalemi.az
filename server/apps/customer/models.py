from django.db import models


class Customer(models.Model):
    """Model definition for Customer."""

    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        return self.name
    
    @property
    def total(self):
        return sum(sale.total for sale in self.sales.all())
    
    @property
    def paid(self):
        return sum(sale.paid for sale in self.sales.all())
    
    @property
    def debt(self):
        return sum(sale.debt for sale in self.sales.all())
    
    @property
    def last_sale(self):
        return self.sales.last()
