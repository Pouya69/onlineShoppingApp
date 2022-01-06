from django.contrib.auth.models import User
from django.db import models


CANADA_PROVINCES = [
    ("AB","ab"),
    ("BC","bc"),
    ("MB","mb"),
    ("NB","nb"),
    ("NL","nl"),
    ("NS","ns"),
    ("ON","on"),
    ("PE","pe"),
    ("QC","Qc"),
    ("SK","sk"),
    ("NT","nt"),
    ("NU","nu"),
    ("YT","yt"),
]


# These are just some dummy tax rates lol
TAX_RATES = {
    "AB": 0.1,
    "BC": 0.12,
    "MB": 0.09,
    "NB": 0.05,
    "NL": 0.01,
    "NS": 0.2,
    "ON": 0.18,
    "PE": 0.17,
    "QC": 0.16,
    "SK": 0.14,
    "NT": 0.12,
    "NU": 0.1,
    "YT": 0.3,
}


class UserApp(models.Model):
    
    original_user = models.ForeignKey(User, related_name="django_user", on_delete=models.CASCADE, blank=False, null=False)
    orders = models.ManyToManyField('Order', related_name="orders_history", default=None, blank=True)
    shopping_cart = models.ManyToManyField('Product',  related_name="products_in_cart", default=None, blank=True)
    comments = models.ManyToManyField('Comment', related_name="user_comments_products", default=None, blank=True)
    province = models.TextField(blank=False, choices=CANADA_PROVINCES)

    def __str__(self):
        return self.original_user.username


class Comment(models.Model):
    user = models.ForeignKey(UserApp, related_name="user_commented", on_delete=models.CASCADE, blank=False, null=False)
    comment_text = models.TextField(max_length=1000, blank=False, null=False)
    comment_date = models.DateField(blank=False, auto_now_add=True)

    def __str__(self):
        return self.comment_text


class Product(models.Model):
    CATEGORIES = [
        ("electronics", "Electronics"),
        ("entertainment", "Entertainment"),
        ("books", "Books"),
    ]

    added_date = models.DateField(blank=False, auto_now_add=True)
    name = models.CharField(blank=False, max_length=25)
    category = models.CharField(default="", max_length=20, blank=False, choices=CATEGORIES)
    price = models.DecimalField(blank=False, max_digits=7, decimal_places=2)
    review_score = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.ImageField(upload_to='pics/', blank=True, null=True, default=None)
    comments = models.ManyToManyField(Comment, related_name="comments_of_users", default=None, blank=True)

    def __str__(self):
        return self.name

    def get_latest_products(self, product_type=None, start=0, end=20):
        if product_type:
            return self.objects.filter(category=product_type).order_by('-id')[start:end][::-1]
        return self.objects.all().order_by('-id')[start:end][::-1]
        


class Order(models.Model):
    SHIPPING_TYPES = [
        ("standard", "Standard"),
        ("premium", "Premium")
    ]

    order_date = models.DateField(blank=False, auto_now_add=True)
    products = models.ManyToManyField(Product, related_name="products_bought", default=None, blank=True)
    ordered_by_user = models.ForeignKey(UserApp, related_name="user_ordered", on_delete=models.CASCADE, blank=False, null=False)
    address = models.TextField(blank=False)
    description = models.TextField(default="", max_length=2000)
    shipping_type = models.CharField(max_length=9, blank=False, choices=SHIPPING_TYPES)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, blank=False)  # With tax and shipping
    done = models.BooleanField(default=False)

