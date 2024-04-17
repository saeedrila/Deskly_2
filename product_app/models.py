from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="categories")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to="sub_categories")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="brands")
    is_active = models.BooleanField(default=True)
    offer_is_active = models.BooleanField(default=False)
    offer_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    mrp = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products")
    availability = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    sell_count = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    varient = models.CharField(max_length=20, default="Basic")
    offer_is_active = models.BooleanField(default=False)
    offer_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Subproduct(models.Model):
    product = models.ForeignKey(
        Product, related_name="subproducts", on_delete=models.CASCADE
    )
    subproduct_id = models.CharField(max_length=50)
    mrp = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    sell_count = models.PositiveIntegerField(default=0)
    varient = models.CharField(max_length=20)
    offer_is_active = models.BooleanField(default=False)
    offer_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Subproduct {self.subproduct_id} of {self.product.name}"


def product_image_upload_to(instance, filename):
    product_name = instance.product.name.replace(" ", "_")
    return f"products/{product_name}_{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=product_image_upload_to)

    def __str__(self):
        return f"Image for {self.product.name}"


# Sample model to check search autosuggestion
class Names(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Sample model to check image cropping
class Image(models.Model):
    file = models.ImageField(upload_to="images")
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
