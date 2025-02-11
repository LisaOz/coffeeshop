from django.db import models
from django.urls import reverse

# Create your models here.

"""
Category model. This model consists of a name field and a unique slug field
"""


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)


    # Add absolute URL to the product_list.
    # 'get_absolute_url' is a convention for retrieving of the URL for the given object
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )

    """
    Define the index for the name field
    """

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']), ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


"""
Product model with fields category (Foreign Key to the Category model, one-to-many relationship; name, slug, image, description, price, availability, created, updated).
"""


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE)

    name = models.CharField(max_length=200) # name of the product in the Menu
    slug = models.SlugField(max_length=200) # slug to build a good looking url
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) # image of the product in the menu
    description = models.TextField(blank=True) # product description; blank on default
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)  # Use DecimalField instead of FloatField to avoid rounding.
    available = models.BooleanField(default=True) # Boolean to display if the product available or not
    created = models.DateTimeField(auto_now_add=True) # date of creation
    updated = models.DateTimeField(auto_now=True) # date of updating
    size = models.CharField(max_length=50, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
                            default='medium')
    temperature = models.CharField(max_length=50, choices=[('hot', 'Hot'), ('cold', 'Cold')], default='hot')
    vegan = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    """
    Define a multiple field index for the id and slug fields indexed together as we plan to query products by both id and slug; one to many relationship.
    """

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
