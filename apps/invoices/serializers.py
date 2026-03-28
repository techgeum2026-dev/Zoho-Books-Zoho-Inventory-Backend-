# from rest_framework import serializers
# from .models import Invoice, InvoiceItem
# from apps.items.models import Item


# class InvoiceItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InvoiceItem
#         fields = ['item', 'quantity', 'rate', 'amount']
#         read_only_fields = ['rate', 'amount']


# class InvoiceSerializer(serializers.ModelSerializer):
#     items = InvoiceItemSerializer(many=True)

#     class Meta:
#         model = Invoice
#         fields = '__all__'

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')

#         invoice = Invoice.objects.create(**validated_data)

#         total = 0

#         for item_data in items_data:
#             item_obj = Item.objects.get(id=item_data['item'].id)

#             rate = item_obj.unit_price
#             quantity = item_data['quantity']
#             amount = rate * quantity

#             InvoiceItem.objects.create(
#                 invoice=invoice,
#                 item=item_obj,
#                 quantity=quantity,
#                 rate=rate,
#                 amount=amount
#             )

#             total += amount

#         invoice.total_amount = total
#         invoice.save()

#         return invoice