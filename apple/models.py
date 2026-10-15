from django.db import models

class customer(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()
    customer_password = models.CharField(max_length=100)
    customer_place = models.CharField(max_length=100)

class Order(models.Model):
    STATUS = [("created", "Created"), ("paid", "Paid"), ("failed", "Failed")]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    car_brand = models.CharField(max_length=100)
    car_name = models.CharField(max_length=100)
    car_color = models.CharField(max_length=50)
    car_price = models.CharField(max_length=50)
    amount_paise = models.PositiveIntegerField()
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_inr(self):
        return f"{self.amount_paise // 100:,}"

    def __str__(self):
        return f"{self.name} - {self.car_name} ({self.status})"