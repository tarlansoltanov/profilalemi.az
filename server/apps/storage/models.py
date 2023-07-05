from django.db import models


class Storage(models.Model):
    """Model definition for Storage."""

    product = models.ForeignKey("product.Product", verbose_name="Product", on_delete=models.CASCADE, related_name="storage")
    quantity = models.IntegerField(verbose_name="Quantity")
    buy_price = models.DecimalField(verbose_name="Buy price", max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(verbose_name="Sell price", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Storage."""

        verbose_name = 'Storage Item'
        verbose_name_plural = 'Storage'

    def __str__(self):
        """Unicode representation of Storage."""
        return f"{self.product} - {self.quantity} - {self.buy_price} - {self.sell_price}"
    
    @property
    def sold(self):
        return self.salestorages.all().aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    
    @property
    def left(self):
        return self.quantity - self.sold
