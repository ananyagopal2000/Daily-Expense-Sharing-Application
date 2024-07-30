from django.db import models
import uuid
import jsonfield

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20)
    
class Expense(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_id = models.UUIDField(default=uuid.uuid4, unique=True, editable= False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=[('equal','Equal'),('exact','Exact'),('percentage','Percentage')])
    date = models.DateTimeField(auto_now_add=True)
    
class SplitDetails(models.Model):
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Unpaid")
    date = models.DateTimeField(auto_now_add=True)