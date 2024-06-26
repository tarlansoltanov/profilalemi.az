from django.db import models

class Product(models.Model):
    """Model definition for Product."""

    name = models.ForeignKey("ProductName", verbose_name="Name", on_delete=models.CASCADE, related_name="products")
    color = models.ForeignKey("color.Color", verbose_name="Color", on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return f"{self.name} - {self.color}"
    
    def save(self, *args, **kwargs):
        old_product = Product.objects.get(pk=self.pk) if self.pk else None
        super(Product, self).save(*args, **kwargs)
        if old_product:
            if old_product.name.products.count() == 0:
                old_product.name.delete()
            if old_product.color.products.count() == 0:
                old_product.color.delete()
    
    @property
    def total_quantity(self):
        quantity = self.storage.aggregate(models.Sum('quantity'))['quantity__sum']
        return quantity or 0
    
    @property
    def sold(self):
        return sum(item.sold for item in self.storage.all())
    
    @property
    def left(self):
        return self.total_quantity - self.sold
    
    @property
    def price(self):
        last = self.storage.last()
        return last.sell_price if last else 0
    
    @property
    def last_in(self):
        last = self.storage.last()
        return last.created_at if last else None


class ProductName(models.Model):
    """Model definition for ProductName."""

    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ProductName."""

        verbose_name = 'Product Name'
        verbose_name_plural = 'Product Names'

    def __str__(self):
        """Unicode representation of ProductName."""
        return self.name