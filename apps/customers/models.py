# from django.db import models

# class Customer(models.Model):
#     CUSTOMER_TYPE_CHOICES = [
#         ('INDIVIDUAL', 'Individual'),
#         ('BUSINESS', 'Business'),
#     ]

#     name = models.CharField(max_length=255)

#     email = models.EmailField(blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)

#     customer_type = models.CharField(
#         max_length=20,
#         choices=CUSTOMER_TYPE_CHOICES,
#         default='INDIVIDUAL'
#     )

#     credit_limit = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True
#     )

#     address = models.TextField(blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
#     class Meta:
#         db_table = 'customers'