# from django.db import models
# from apps.customers.models import Customer
# from apps.items.models import Item


# class Invoice(models.Model):
#     STATUS_CHOICES = [
#         ('DRAFT', 'Draft'),
#         ('SENT', 'Sent'),
#         ('PARTIALY PAID','Partially Paid'),
#         ('PAID', 'Paid'),
#     ]

#     customer = models.ForeignKey(
#         Customer,
#         on_delete=models.CASCADE,
#         related_name='invoices'
#     )

#     invoice_number = models.CharField(max_length=50, unique=True)

#     date = models.DateField()

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='DRAFT'
#     )

#     total_amount = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         default=0
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.invoice_number


# class InvoiceItem(models.Model):
#     invoice = models.ForeignKey(
#         Invoice,
#         on_delete=models.CASCADE,
#         related_name='items'
#     )

#     item = models.ForeignKey(
#         Item,
#         on_delete=models.CASCADE
#     )

#     quantity = models.DecimalField(max_digits=10, decimal_places=2)

#     rate = models.DecimalField(max_digits=10, decimal_places=2)

#     amount = models.DecimalField(max_digits=12, decimal_places=2)

#     def __str__(self):
#         return f"{self.invoice.invoice_number} - {self.item.name}"