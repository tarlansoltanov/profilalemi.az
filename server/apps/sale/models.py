from django.db import models
                     

class SaleStorage(models.Model):
    """Model definition for SaleStorage."""

    sale = models.ForeignKey('Sale', verbose_name="Sale", on_delete=models.CASCADE, related_name='salestorages')
    storage = models.ForeignKey('storage.Storage', verbose_name="Storage", on_delete=models.CASCADE, related_name='salestorages')
    quantity = models.IntegerField(verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        """Meta definition for SaleStorage."""

        verbose_name = 'SaleStorage'
        verbose_name_plural = 'SaleStorages'

    def __str__(self):
        """Unicode representation of SaleStorage."""
        return f"{self.sale} - {self.storage}"
    
    @property
    def income(self):
        return self.quantity * self.sale.sell_price - self.storage.buy_price * self.quantity


class Sale(models.Model):
    """Model definition for Sale."""

    storage = models.ManyToManyField('storage.Storage', through='SaleStorage', verbose_name="Storage", related_name='sales')
    customer = models.ForeignKey('customer.Customer', verbose_name="Customer", on_delete=models.CASCADE, related_name='sales')
    quantity = models.IntegerField(verbose_name="Quantity")
    sell_price = models.DecimalField(verbose_name="Sell Price", max_digits=10, decimal_places=2)
    paid = models.DecimalField(verbose_name="Paid", max_digits=10, decimal_places=2)
    user = models.ForeignKey('auth.User', verbose_name="User", on_delete=models.CASCADE, related_name='sales')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Sale."""

        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self):
        """Unicode representation of Sale."""
        return f"{self.customer} - {self.quantity} - {self.sell_price}"
    
    def create_salestorage(self, product):
        storages = product.storage.all().order_by('created_at')
        for storage in storages:
            if storage.left >= self.quantity:
                SaleStorage.objects.create(sale=self, storage=storage, quantity=self.quantity)
                break
            else:
                SaleStorage.objects.create(sale=self, storage=storage, quantity=storage.left)
                self.quantity -= storage.left
    
    def save(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        if self.pk:
            self.salestorages.all().delete()
        
        if product:
            self.create_salestorage(product)
        
        super().save(*args, **kwargs)
    
    @property
    def total(self):
        return self.quantity * self.sell_price
    
    @property
    def debt(self):
        return self.total - self.paid
    
    @property
    def storages(self):
        return self.salestorages.all()
    
    @property
    def product(self):
        return self.storages.first().storage.product if self.storages.first() else None
    
    @property
    def income(self):
        return sum(s.income for s in self.storages.all()) or 0
